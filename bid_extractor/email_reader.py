import time
import datetime
import traceback
import imbox
from imaplib import IMAP4
from .local_settings import (
    HOST,
    USERNAME,
    PASSWORD,
    POLLING_INTERVAL,
    SEARCH_EMAIL,
    DOWNLOAD_FOLDER,
    DATABASE,
)
from .schmitz import extract_price
from .database_interface import create_connection, enter_grain_bids


def connect_to_mailbox(host=HOST, username=USERNAME, password=PASSWORD):
    mail = imbox.Imbox(
        HOST,
        username=USERNAME,
        password=PASSWORD,
        ssl=True,
        ssl_context=None,
        starttls=False,
    )
    return mail


def process_attachments(message):
    attachments = []
    for idx, attachment in enumerate(message.attachments):
        try:
            att_fn = attachment.get("filename")
            download_path = f"{DOWNLOAD_FOLDER}/{idx}_{att_fn}"
            with open(download_path, "wb") as fp:
                fp.write(attachment.get("content").read())
            attachments.append(download_path)
        except:
            print(traceback.print_exc())
    return attachments


def process_messages(mail, db):
    try:
        messages = mail.messages(
            date__gt=datetime.date(2024, 4, 5),  # inclusive
            date__lt=datetime.date(2024, 4, 6),  # exclusive
            sent_from=SEARCH_EMAIL,
        )
        for (uid, message) in messages:
            sent_from = message.sent_from[0]["name"]
            subject = message.subject
            print(f"Reading email {subject} from {sent_from}")
            message_date = message.parsed_date.strftime("%Y-%m-%d")
            filename = f"{DOWNLOAD_FOLDER}/{message_date}-Elevator_Bids.html"
            with open(filename, "w") as f:
                f.write(
                    str(message.body["html"])
                    .replace("\\r", " ")
                    .replace("\\n", " ")
                    .replace("['", "")
                    .replace("']", "")
                )
            prices = extract_price(f"file://{filename}", message.parsed_date)
            if prices != None:
                price_date = message.parsed_date.strftime("%Y-%m-%d %H:%M:%S")
                for key in prices.keys():
                    insert_idx = enter_grain_bids(db, key, price_date, prices[key])
                    print(f"Row inserted into database at index {insert_idx}")
            mail.mark_seen(uid)
            mail.delete(uid)
        return 0
    except (ConnectionResetError, IMAP4.abort) as e:
        print("Connection Reset, waiting for five minutes before retrying...")
        time.sleep(300)  # Wait 5 minutes before trying again
        return -1


# Set up connections
mail = connect_to_mailbox()
gnucash = create_connection(DATABASE)

while True:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"{current_time} - Checking for messages...")
    if process_messages(mail, gnucash) < 0:
        # Connection Reset, recreate mail object
        del mail
        mail = connect_to_mailbox()
    else:
        # set POLLING_INTERVAL to 0 to run just once
        if POLLING_INTERVAL == 0:
            print(f"{current_time} - Done processing!")
            break
        else:
            print(f"{current_time} - Waiting {POLLING_INTERVAL} seconds...")
            time.sleep(POLLING_INTERVAL)

mail.logout()

import os
import time
import datetime
import traceback
from imbox import Imbox
from imaplib import IMAP4
from .local_settings import (
    HOST,
    USERNAME,
    PASSWORD,
    POLLING_INTERVAL,
    SEARCH_EMAIL,
    DOWNLOAD_FOLDER,
)


def connect_to_mailbox(host=HOST, username=USERNAME, password=PASSWORD):
    mail = Imbox(
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


def process_unread_messages(mail):
    try:
        # messages = mail.messages(unread=True)  # defaults to inbox
        messages = mail.messages(
            date__gt=datetime.date(2021, 11, 1), sent_from=SEARCH_EMAIL
        )

        for (uid, message) in messages:
            print(uid)
            sent_from = message.sent_from[0]["name"]
            subject = message.subject
            print(f"Reading email {subject} from {sent_from}")
            # message_date = timestring.Date(year, month, day, hour, minute, second)(message.date)
            message_date = message.parsed_date.strftime("%Y-%m-%d")
            filename = f"{message_date}-Schmitz_Grain_Bids.html"
            with open(filename, "w") as f:
                f.write(
                    str(message.body["html"])
                    .replace("\\r", " ")
                    .replace("\\n", " ")
                    .replace("['", "")
                    .replace("']", "")
                )
            # attachments = process_attachments(message)

            # mail.mark_seen(uid)  # mark message as read
        return 0
    except (ConnectionResetError, IMAP4.abort) as e:
        print(e)
        print("Connection Reset, waiting for five minutes before retrying...")
        time.sleep(300)  # Wait 5 minutes before trying again
        return -1


mail = connect_to_mailbox()

while True:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"{current_time} - Checking for new messages...")
    if process_unread_messages(mail) < 0:
        # Connection Reset, recreate mail object
        del mail
        mail = connect_to_mailbox()
    else:
        time.sleep(POLLING_INTERVAL)

mail.logout()

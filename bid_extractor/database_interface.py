import uuid
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def enter_grain_bids(conn, commodity, date, price):
    """
    Create a new task
    :param conn:
    :param commodity:
    :param date:
    :param price:
    :return:
    """
    COMMODITY_GUID = {"corn": '9674359206294b7293e00c8bc317b9b0',
                      "soybeans": '05b83824752d49039bd436244c4f4729',
                     }
    CURRENCY_GUID = 'a5cb4782e9d344e693e7c99cb35eb687'
    SOURCE = 'user:price-editor'
    PRICE_TYPE = 'bid'
    VALUE_DENOM = 100

    sql = f"""insert into prices (guid,
                                 commodity_guid, 
                                 currency_guid, 
                                 date, 
                                 source, 
                                 type, 
                                 value_num, 
                                 value_denom)
             VALUES ('{uuid.uuid4().hex}',
                     '{COMMODITY_GUID[commodity]}',
                     '{CURRENCY_GUID}',
                     '{date}',
                     '{SOURCE}',
                     '{PRICE_TYPE}',
                     {price},
                     {VALUE_DENOM})
            """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

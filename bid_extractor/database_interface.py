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
    COMMODITY_GUID = {"corn": '05b83824752d49039bd436244c4f4729',
                      "soybeans": '9674359206294b7293e00c8bc317b9b0'
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
    return sql
    # cur = conn.cursor()
    # cur.execute(sql)
    # conn.commit()
    # return cur.lastrowid


"""
def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        project_id = create_project(conn, project)

        # tasks
        task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)
"""

if __name__ == '__main__':
    # main()
    print(enter_grain_bids("hi", "soybeans", "2021-02-10", 558))

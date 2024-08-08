import mysql.connector
from config_oli import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=db_name
    )
    return cnx


def add_new_data(id, name, email):

    try:
        db_name = 'customer_details'
        db_connection = _connect_to_db(db_name)
        cur = db_connection.cursor()

        query = f"""INSERT INTO emails (id, first_name, email_address)
                VALUES(
                '{id}',
                '{name}',
                '{email}')"""

        cur.execute(query)
        db_connection.commit()
        print("New customer details added")
        cur.close()

    except Exception:
        raise DbConnectionError("Failed to write data to DB")
    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def main():
    add_new_data(21, "Kate", "katie_holmes@example.com")


if __name__ == '__main__':
    main()
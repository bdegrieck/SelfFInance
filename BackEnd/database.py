import mysql.connector
from mysql.connector import Error


def connect():
    """ Connect to MySQL database """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Apple',
            user='root',
            password='M@ggie01'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            # Example query
            cursor.execute("SELECT * FROM your_table_name;")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == "__main__":
    connect()

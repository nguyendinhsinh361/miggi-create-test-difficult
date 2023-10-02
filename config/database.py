import mysql.connector


def connect_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='hsk'
    )
    return conn

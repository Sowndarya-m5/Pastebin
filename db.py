import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sownd@05",
        database="pastebin"
    )


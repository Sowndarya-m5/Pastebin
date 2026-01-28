import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["localhost"],
        user=os.environ["root"],
        password=os.environ["Sownd@05"],
        database=os.environ["pastebin"],
        port=int(os.environ.get("DB_PORT", 3306))
    )


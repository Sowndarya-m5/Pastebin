# import mysql.connector
# from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# def get_db_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Sownd@05",
#         database="pastebin"
#     )





import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("localhost"),
        database=os.environ.get("pastedb"),
        user=os.environ.get("postgres"),
        password=os.environ.get("Sownd@05"),
        port=os.environ.get("DB_PORT", 5432)  # default PostgreSQL port
    )
    return conn

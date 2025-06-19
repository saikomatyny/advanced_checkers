import psycopg2
from config import DB_USER, DB_PASSWORD

def connect_database():
    conn = psycopg2.connect(
        dbname = "checkers",
        user = DB_USER,
        password = DB_PASSWORD,
        host = "localhost",
        port = "5433"
    )
    cur = conn.cursor() # cusror for DataBase

    return cur

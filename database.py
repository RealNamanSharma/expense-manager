import os
import psycopg

def get_connection():
    return psycopg.connect(os.environ["DB_URL"])

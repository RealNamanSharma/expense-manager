import psycopg

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="expense_tracker",
        user="postgres",
        password="1234567890",
        port=5432
    )
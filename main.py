from fastapi import FastAPI
from models import Expense
from database import get_connection

app = FastAPI()



@app.get("/")
def home():
    return {"message": "Welcome to Expense Tracker API"}



@app.get("/expenses")
def get_expenses():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM expenses")
            data = cur.fetchall()

    return data


@app.post("/expenses")
def add_expense(exp: Expense):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO expenses
                (id, title, amount, category, expense_date)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    exp.id,
                    exp.title,
                    exp.amount,
                    exp.category,
                    exp.expense_date
                )
            )

            data = cur.fetchone()

    return data



@app.get("/expenses/by-date/{date}")
def get_expenses_by_date(date: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM expenses WHERE expense_date = %s",
                (date,)
            )

            data = cur.fetchall()

    return data


@app.delete("/expenses/{e_id}")
def delete_expense(e_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM expenses
                WHERE id = %s
                RETURNING *
                """,
                (e_id,)
            )

            data = cur.fetchone()

    if data is None:
        return {"message": "ID not found"}

    return data

@app.get("/expenses/total_expense")
def total_expense():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM expenses"
            )

            data = cur.fetchone()

    return {"total_expense": data[0]}


@app.get("/expenses/date/{date}/total_expense")
def total_expense_by_date(date: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE expense_date = %s
                """,
                (date,)
            )

            data = cur.fetchone()

    return {"total_expense": data[0]}

@app.get("/expenses/category/{cat}/total_expense")
def total_expense_by_category(cat: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                FROM expenses
                WHERE category = %s
                """,
                (cat,)
            )

            data = cur.fetchone()

    return {"total_expense": data[0]}

@app.get("/expenses/average_daily_expense")
def average_daily_expense():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(AVG(daily_total), 0)
                FROM (
                    SELECT SUM(amount) AS daily_total
                    FROM expenses
                    GROUP BY expense_date
                ) AS daily_expenses
                """
            )

            data = cur.fetchone()

    return {"average_daily_expense": data[0]}


@app.put("/expenses/{id}")
def update_expense(id: int, exp: Expense):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE expenses
                SET title = %s,
                    amount = %s,
                    category = %s,
                    expense_date = %s
                WHERE id = %s
                RETURNING *
                """,
                (
                    exp.title,
                    exp.amount,
                    exp.category,
                    exp.expense_date,
                    id
                )
            )

            data = cur.fetchone()

    if data is None:
        return {"message": "Not updated: ID not found"}

    return data
from pydantic import BaseModel
from datetime import date

class Expense(BaseModel):
    id: int
    title: str
    amount: int
    category: str
    expense_date: date

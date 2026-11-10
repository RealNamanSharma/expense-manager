from pydantic import BaseModel

class Expense(BaseModel):
    id: int
    title: str
    amount: int
    category: str
    expense_date: str
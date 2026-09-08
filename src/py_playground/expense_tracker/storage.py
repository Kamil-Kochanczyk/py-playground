import datetime
import decimal
import json
from pathlib import Path

from py_playground.expense_tracker.expense import Expense, ExpenseDict


def expense_to_dict(expense: Expense) -> ExpenseDict:
    return {
        "id": expense.expense_id,
        "amount": str(expense.amount),
        "category": expense.category,
        "description": expense.description,
        "date": expense.date.isoformat(),
    }


def expense_from_dict(data: ExpenseDict) -> Expense:
    return Expense(
        expense_id=data["id"],
        amount=decimal.Decimal(data["amount"]),
        category=data["category"],
        description=data["description"],
        date=datetime.datetime.fromisoformat(data["date"]),
    )


def save_expenses(expenses: list[Expense], filename: Path) -> None:
    with Path.open(filename, "w") as f:
        json.dump([expense_to_dict(expense) for expense in expenses], f, indent=4)


def load_expenses(filename: Path) -> list[Expense]:
    try:
        with Path.open(filename, "r") as f:
            return [expense_from_dict(data) for data in json.load(f)]
    except FileNotFoundError:
        return []

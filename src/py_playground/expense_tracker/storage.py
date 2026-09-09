"""Persistence helpers for loading and saving expenses as JSON."""

import datetime
import decimal
import json
from pathlib import Path

from py_playground.expense_tracker.expense import Expense, ExpenseDict


def expense_to_dict(expense: Expense) -> ExpenseDict:
    """Convert an Expense instance into a JSON-serializable dictionary.

    Args:
        expense: The expense to serialize.

    Returns:
        A dictionary containing the expense fields in the on-disk format.

    """
    return {
        "id": expense.expense_id,
        "amount": str(expense.amount),
        "category": expense.category,
        "description": expense.description,
        "date": expense.date.isoformat(),
    }


def expense_from_dict(data: ExpenseDict) -> Expense:
    """Reconstruct an Expense instance from a serialized dictionary.

    Args:
        data: The dictionary representation of an expense.

    Returns:
        An Expense instance created from the serialized data.

    """
    return Expense(
        expense_id=data["id"],
        amount=decimal.Decimal(data["amount"]),
        category=data["category"],
        description=data["description"],
        date=datetime.datetime.fromisoformat(data["date"]),
    )


def save_expenses(expenses: list[Expense], filename: Path) -> None:
    """Persist the provided expenses to a JSON file.

    Args:
        expenses: The expenses to write.
        filename: The destination path for the serialized JSON data.

    """
    with Path.open(filename, "w") as f:
        json.dump([expense_to_dict(expense) for expense in expenses], f, indent=4)


def load_expenses(filename: Path) -> list[Expense]:
    """Load expenses from a JSON file if it exists.

    Args:
        filename: The path to the JSON file containing expenses.

    Returns:
        A list of Expense instances loaded from disk, or an empty list when the file
        does not exist.

    """
    try:
        with Path.open(filename, "r") as f:
            return [expense_from_dict(data) for data in json.load(f)]
    except FileNotFoundError:
        return []

import datetime
import decimal

import pytest

from py_playground.expense_tracker.expense import Expense


@pytest.fixture(scope="module")
def example_expenses():
    return [
        Expense(
            expense_id=0,
            amount=decimal.Decimal("100.0"),
            category="food",
            description="Breakfast",
            date=datetime.datetime(2026, 8, 30, tzinfo=datetime.UTC),
        ),
        Expense(
            expense_id=1,
            amount=decimal.Decimal("1000.0"),
            category="transport",
            description="Travel",
            date=datetime.datetime(2026, 8, 15, tzinfo=datetime.UTC),
        ),
        Expense(
            expense_id=5,
            amount=decimal.Decimal("200.0"),
            category="food",
            description="Dinner",
            date=datetime.datetime(2026, 8, 29, tzinfo=datetime.UTC),
        ),
        Expense(
            expense_id=4,
            amount=decimal.Decimal("500.0"),
            category="entertainment",
            description="Cinema",
            date=datetime.datetime(2026, 8, 1, tzinfo=datetime.UTC),
        ),
    ]


@pytest.fixture(scope="module")
def example_food_expenses(example_expenses):
    return [expense for expense in example_expenses if expense.category == "food"]

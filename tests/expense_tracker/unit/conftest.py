import datetime
import decimal

import pytest

from py_playground.expense_tracker.expense import Expense


@pytest.fixture(scope="module")
def example_expenses():
    return [
        Expense(
            0,
            decimal.Decimal("100.0"),
            "food",
            "Breakfast",
            datetime.datetime(2026, 8, 30, tzinfo=datetime.UTC),
        ),
        Expense(
            1,
            decimal.Decimal("1000.0"),
            "transport",
            "Travel",
            datetime.datetime(2026, 8, 15, tzinfo=datetime.UTC),
        ),
        Expense(
            5,
            decimal.Decimal("200.0"),
            "food",
            "Dinner",
            datetime.datetime(2026, 8, 29, tzinfo=datetime.UTC),
        ),
        Expense(
            4,
            decimal.Decimal("500.0"),
            "entertainment",
            "Cinema",
            datetime.datetime(2026, 8, 1, tzinfo=datetime.UTC),
        ),
    ]


@pytest.fixture(scope="module")
def example_food_expenses(example_expenses):
    return [expense for expense in example_expenses if expense.category == "food"]

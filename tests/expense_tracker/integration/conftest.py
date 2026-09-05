import datetime
import decimal

import pytest

from py_playground.expense_tracker.expense import Expense


@pytest.fixture
def tmp_json_path(tmp_path):
    return tmp_path / "expenses.json"


@pytest.fixture(scope="module")
def example_expenses():
    return [
        Expense(
            10,
            decimal.Decimal("10.0"),
            "food",
            "Breakfast",
            datetime.datetime(2002, 8, 30, tzinfo=datetime.UTC),
        ),
        Expense(
            11,
            decimal.Decimal("100.0"),
            "transport",
            "Travel",
            datetime.datetime(2002, 8, 15, tzinfo=datetime.UTC),
        ),
        Expense(
            15,
            decimal.Decimal("20.0"),
            "food",
            "Dinner",
            datetime.datetime(2002, 8, 29, tzinfo=datetime.UTC),
        ),
        Expense(
            14,
            decimal.Decimal("50.0"),
            "entertainment",
            "Cinema",
            datetime.datetime(2002, 8, 1, tzinfo=datetime.UTC),
        ),
    ]

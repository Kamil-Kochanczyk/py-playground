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
            expense_id=10,
            amount=decimal.Decimal("10.0"),
            category="food",
            description="Breakfast",
            date=datetime.datetime(2002, 8, 30, tzinfo=datetime.UTC),
        ),
        Expense(
            expense_id=11,
            amount=decimal.Decimal("100.0"),
            category="transport",
            description="Travel",
            date=datetime.datetime(2002, 8, 15, tzinfo=datetime.UTC),
        ),
        Expense(
            expense_id=15,
            amount=decimal.Decimal("20.0"),
            category="food",
            description="Dinner",
            date=datetime.datetime(2002, 8, 29, tzinfo=datetime.UTC),
        ),
        Expense(
            expense_id=14,
            amount=decimal.Decimal("50.0"),
            category="entertainment",
            description="Cinema",
            date=datetime.datetime(2002, 8, 1, tzinfo=datetime.UTC),
        ),
    ]

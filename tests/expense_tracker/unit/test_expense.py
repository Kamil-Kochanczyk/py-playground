import datetime
import decimal

import pytest

from py_playground.expense_tracker.expense import Expense


def test_expense_not_valid_amount():
    with pytest.raises(decimal.InvalidOperation, match="ConversionSyntax"):
        Expense(
            expense_id=0,
            amount=decimal.Decimal("abc"),
            category="",
            description="",
            date=datetime.datetime.min.replace(tzinfo=datetime.UTC),
        )


def test_expenses_equal(example_expenses):
    test_expenses = [
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

    assert len(test_expenses) == len(example_expenses)

    n = len(test_expenses)

    for i in range(n):
        assert test_expenses[i] == example_expenses[i]


def test_expenses_not_equal(example_expenses):
    test_expenses = [
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

    assert len(test_expenses) == len(example_expenses)

    n = len(test_expenses)

    for i in range(n):
        assert test_expenses[i] != example_expenses[i]

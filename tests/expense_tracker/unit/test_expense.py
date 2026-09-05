import datetime
import decimal

import pytest

from py_playground.expense_tracker.expense import Expense


def test_expense_not_valid_amount():
    with pytest.raises(decimal.InvalidOperation, match="ConversionSyntax"):
        Expense(
            0,
            decimal.Decimal("abc"),
            "",
            "",
            datetime.datetime.min.replace(tzinfo=datetime.UTC),
        )


def test_expenses_equal(example_expenses):
    test_expenses = [
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

    assert len(test_expenses) == len(example_expenses)

    n = len(test_expenses)

    for i in range(n):
        assert test_expenses[i] == example_expenses[i]


def test_expenses_not_equal(example_expenses):
    test_expenses = [
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

    assert len(test_expenses) == len(example_expenses)

    n = len(test_expenses)

    for i in range(n):
        assert test_expenses[i] != example_expenses[i]

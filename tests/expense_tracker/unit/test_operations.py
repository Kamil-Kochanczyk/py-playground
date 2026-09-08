import copy
import decimal

import pytest

from py_playground.expense_tracker import operations
from py_playground.expense_tracker.expense import Expense


@pytest.mark.parametrize(
    ("existing_ids", "expected_next_id"),
    [([], 0), ([0, 1, 2], 3), ([0, 5, 2], 6)],
    ids=["empty", "012->3", "052->6"],
)
def test_generate_next_id(existing_ids, expected_next_id, expense_factory_id):
    expenses = []
    for existing_id in existing_ids:
        expenses.append(expense_factory_id(existing_id))
    assert operations.generate_next_id(expenses) == expected_next_id


def test_add_expense(example_expenses):
    some_expenses = copy.deepcopy(example_expenses)
    some_expenses_expected = copy.deepcopy(some_expenses)
    some_expenses_expected.append(Expense.dummy_expense())
    operations.add_expense(some_expenses, Expense.dummy_expense())
    assert len(some_expenses) == len(some_expenses_expected)
    for expense, expense_expected in zip(some_expenses, some_expenses_expected, strict=True):
        assert expense == expense_expected


@pytest.mark.parametrize(
    ("existing_ids_before", "id_to_delete", "expected_bool", "expected_ids_after"),
    [
        ([], 100, False, []),
        ([0, 1, 2], 1, True, [0, 2]),
        ([0, 5, 2], 6, False, [0, 5, 2]),
        ([0, 5, 2], 5, True, [0, 2]),
    ],
    ids=["empty", "012->1->02", "052->6->052", "052->5->02"],
)
def test_delete_expense(
    existing_ids_before,
    id_to_delete,
    expected_bool,
    expected_ids_after,
    expense_factory_id,
):
    expenses = []
    for existing_id_before in existing_ids_before:
        expenses.append(expense_factory_id(existing_id_before))
    bool_res = operations.delete_expense(expenses, id_to_delete)
    new_ids = [expense.expense_id for expense in expenses]
    assert bool_res == expected_bool
    assert new_ids == expected_ids_after


@pytest.mark.parametrize(
    ("id_to_get", "expected_res_idx"),
    [(5, 2), (10, None)],
    ids=["id5-idx2", "id10-idxNone"],
)
def test_get_expense(id_to_get, expected_res_idx, example_expenses):
    if expected_res_idx is None:
        assert operations.get_expense(example_expenses, id_to_get) is None
    else:
        assert operations.get_expense(example_expenses, id_to_get) == example_expenses[expected_res_idx]


@pytest.mark.parametrize(
    ("existing_categories", "filter_category", "expected_category_count"),
    [
        (["food", "transport", "food"], "food", 2),
        ([], "entertainment", 0),
        (["food", "transport", "food"], "Food", 0),
    ],
    ids=["food-2", "empty", "Food-0"],
)
def test_filter_by_category(
    existing_categories,
    filter_category,
    expected_category_count,
    expense_factory_category,
    example_food_expenses,
):
    expenses = []
    for existing_category in existing_categories:
        expenses.append(expense_factory_category(existing_category))
    filtered = operations.filter_by_category(expenses, filter_category)
    assert len(filtered) == expected_category_count
    assert all(expense.category == filter_category for expense in filtered)
    if filter_category == "food":
        assert len(filtered) == len(example_food_expenses)
        for filtered_expense, example_food_expense in zip(filtered, example_food_expenses, strict=True):
            assert filtered_expense.category == example_food_expense.category


@pytest.mark.parametrize(
    ("existing_amounts", "expected_total"),
    [
        ([], decimal.Decimal("0.0")),
        (
            [decimal.Decimal("100.0"), decimal.Decimal("200.0")],
            decimal.Decimal("300.0"),
        ),
        (
            [decimal.Decimal("100.50"), decimal.Decimal("200.25")],
            decimal.Decimal("300.75"),
        ),
    ],
    ids=["empty-0", "100+200=300", "100.50+200.25=300.75"],
)
def test_calculate_total(existing_amounts, expected_total, expense_factory_amount):
    expenses = []
    for existing_amount in existing_amounts:
        expenses.append(expense_factory_amount(existing_amount))
    assert operations.calculate_total(expenses) == expected_total


@pytest.mark.parametrize(
    ("category", "expected_total"),
    [
        ("Food", decimal.Decimal("0.0")),
        ("food", decimal.Decimal("300.0")),
        ("entertainment", decimal.Decimal("500.0")),
    ],
    ids=[
        "category doesn't exist",
        "category exists food",
        "category exists entertainment",
    ],
)
def test_calculate_category_total(category, expected_total, example_expenses, example_food_expenses):
    assert operations.calculate_category_total(example_expenses, category) == expected_total
    if category == "food":
        assert operations.calculate_category_total(example_expenses, category) == operations.calculate_total(
            example_food_expenses
        )


if __name__ == "__main__":
    pytest.main()

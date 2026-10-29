"""Operations for working with in-memory expense collections."""

from decimal import Decimal
from typing import Literal

from py_playground.expense_tracker.expense import Category, Expense, ExpenseID


def generate_next_id(expenses: list[Expense]) -> ExpenseID:
    """Generate the next available expense ID.

    Args:
        expenses: Existing expenses whose IDs should be considered.

    Returns:
        The next unused expense ID. Returns 0 when the list is empty.

    Examples:
        >>> from py_playground.expense_tracker.expense import Expense
        >>> from py_playground.expense_tracker.operations import generate_next_id
        >>> generate_next_id([])
        0
        >>> expenses = [Expense.dummy_expense(exp_id=2), Expense.dummy_expense(exp_id=5)]
        >>> generate_next_id(expenses)
        6

    """
    if len(expenses) == 0:
        return 0
    return max(expense.expense_id for expense in expenses) + 1


def print_expenses(expenses: list[Expense]) -> None:
    """Print each expense in a compact, readable format.

    Args:
        expenses: The expenses to display.

    """
    for expense in expenses:
        print(
            f"{expense.expense_id}, {expense.amount}, {expense.category}, {expense.description}, {expense.date.strftime('%x')}"
        )


def add_expense(expenses: list[Expense], expense: Expense) -> None:
    """Append a new expense to the given list.

    Args:
        expenses: The list of expenses to update.
        expense: The expense to add.

    Examples:
        >>> from py_playground.expense_tracker.expense import Expense
        >>> from py_playground.expense_tracker.operations import add_expense
        >>> expenses = []
        >>> add_expense(expenses, Expense.dummy_expense(exp_id=1))
        >>> len(expenses)
        1

    """
    expenses.append(expense)


def delete_expense(expenses: list[Expense], id_to_delete: ExpenseID) -> bool:
    """Remove the expense matching the given ID.

    Args:
        expenses: The list of expenses to update.
        id_to_delete: The expense ID to remove.

    Returns:
        True if an expense was removed; otherwise False.

    Examples:
        >>> from py_playground.expense_tracker.expense import Expense
        >>> from py_playground.expense_tracker.operations import delete_expense
        >>> expenses = [Expense.dummy_expense(exp_id=1)]
        >>> delete_expense(expenses, 1)
        True
        >>> delete_expense(expenses, 2)
        False

    """
    for expense in expenses:
        if expense.expense_id == id_to_delete:
            expenses.remove(expense)
            return True
    return False


def get_expense(expenses: list[Expense], id_to_get: ExpenseID) -> Expense | None:
    """Look up an expense by ID.

    Args:
        expenses: The list of expenses to search.
        id_to_get: The expense ID to retrieve.

    Returns:
        The matching Expense instance, or None if no match exists.

    Examples:
        >>> from py_playground.expense_tracker.expense import Expense
        >>> from py_playground.expense_tracker.operations import get_expense
        >>> expenses = [Expense.dummy_expense(exp_id=1)]
        >>> get_expense(expenses, 1).expense_id
        1
        >>> get_expense(expenses, 2) is None
        True

    """
    for expense in expenses:
        if expense.expense_id == id_to_get:
            return expense
    return None


def filter_by_category(expenses: list[Expense], category: Category) -> list[Expense]:
    """Return all expenses matching a specific category.

    Args:
        expenses: The expenses to filter.
        category: The category to match.

    Returns:
        A list containing only the expenses whose category equals `category`.

    Examples:
        >>> from py_playground.expense_tracker.expense import Expense
        >>> from py_playground.expense_tracker.operations import filter_by_category
        >>> expenses = [
        ...     Expense.dummy_expense(exp_id=1, cat="food"),
        ...     Expense.dummy_expense(exp_id=2, cat="transport"),
        ... ]
        >>> [expense.expense_id for expense in filter_by_category(expenses, "food")]
        [1]

    """
    return [expense for expense in expenses if expense.category == category]


def calculate_total(expenses: list[Expense]) -> Decimal | Literal[0]:
    """Sum the amounts of all expenses in the list.

    Args:
        expenses: The expenses to total.

    Returns:
        The combined amount of all expenses.

    Examples:
        >>> from decimal import Decimal
        >>> from py_playground.expense_tracker.expense import Expense
        >>> from py_playground.expense_tracker.operations import calculate_total
        >>> expenses = [
        ...     Expense.dummy_expense(amt=Decimal("12.50")),
        ...     Expense.dummy_expense(amt=Decimal("3.00")),
        ... ]
        >>> calculate_total(expenses)
        Decimal('15.50')

    """
    return sum(expense.amount for expense in expenses)


def calculate_category_total(expenses: list[Expense], category: Category) -> Decimal | Literal[0]:
    """Calculate the total for expenses in a single category.

    Args:
        expenses: The expenses to examine.
        category: The category to total.

    Returns:
        The combined amount for expenses in the requested category.

    Examples:
        >>> from decimal import Decimal
        >>> from py_playground.expense_tracker.expense import Expense
        >>> from py_playground.expense_tracker.operations import calculate_category_total
        >>> expenses = [
        ...     Expense.dummy_expense(amt=Decimal("12.50"), cat="food"),
        ...     Expense.dummy_expense(amt=Decimal("3.00"), cat="transport"),
        ... ]
        >>> calculate_category_total(expenses, "food")
        Decimal('12.50')

    """
    return calculate_total(filter_by_category(expenses, category))

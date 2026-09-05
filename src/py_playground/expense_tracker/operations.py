from decimal import Decimal

from py_playground.expense_tracker.expense import Expense


def generate_next_id(expenses: list[Expense]) -> int:
    if len(expenses) == 0:
        return 0
    return max(expense.id for expense in expenses) + 1


def print_expenses(expenses: list[Expense]) -> None:
    for expense in expenses:
        print(
            f"{expense.id}, {expense.amount}, {expense.category}, {expense.description}, {expense.date.strftime('%x')}"
        )


def add_expense(expenses: list[Expense], expense: Expense) -> None:
    expenses.append(expense)


def delete_expense(expenses: list[Expense], id_to_delete: int) -> bool:
    for expense in expenses:
        if expense.id == id_to_delete:
            expenses.remove(expense)
            return True
    return False


def get_expense(expenses: list[Expense], id_to_get: int) -> Expense | None:
    for expense in expenses:
        if expense.id == id_to_get:
            return expense
    return None


def filter_by_category(expenses: list[Expense], category: str) -> list[Expense]:
    return [expense for expense in expenses if expense.category == category]


def calculate_total(expenses: list[Expense]) -> Decimal:
    return sum(expense.amount for expense in expenses)


def calculate_category_total(expenses: list[Expense], category: str) -> Decimal:
    return calculate_total(filter_by_category(expenses, category))

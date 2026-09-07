import datetime
import decimal
from pathlib import Path

from py_playground.expense_tracker import operations, storage
from py_playground.expense_tracker.expense import Category, Description, Expense

BASE_DIR = Path(__file__).parent  # __file__ is the path to the current file (main.py)
FILENAME = BASE_DIR / "data" / "expenses.json"  # "/" is an overloaded operator


def handle_add_expense(expenses: list[Expense]) -> None:
    try:
        new_id = operations.generate_next_id(expenses)
        new_amount = decimal.Decimal(input("Amount: "))
        new_category = Category(input("Category: "))
        new_description = Description(input("Description: "))
        year, month, day = input("Date (yyyy/mm/dd): ").split("/")
        new_date = datetime.datetime(int(year), int(month), int(day), tzinfo=datetime.UTC)
        new_expense = Expense(new_id, new_amount, new_category, new_description, new_date)
        operations.add_expense(expenses, new_expense)
    except ValueError:
        print("Invalid input")


def handle_print_expenses(expenses: list[Expense]) -> None:
    operations.print_expenses(expenses)


def handle_filter_by_category(expenses: list[Expense]) -> None:
    category = Category(input("Category to filter expenses by: "))
    filtered_by_category = operations.filter_by_category(expenses, category)
    operations.print_expenses(filtered_by_category)


def handle_calculate_total(expenses: list[Expense]) -> None:
    total = operations.calculate_total(expenses)
    print("Total: " + str(total))


def handle_calculate_category_total(expenses: list[Expense]) -> None:
    category = Category(input("Category to filter expenses by: "))
    total = operations.calculate_category_total(expenses, category)
    print("Category total: " + str(total))


def handle_delete_expense(expenses: list[Expense]) -> None:
    try:
        id_to_delete = int(input("ID of expense: "))  # type alias not callable so we must use the raw int
        success = operations.delete_expense(expenses, id_to_delete)
        print("Deleted!" if success else "Delete operation unsuccessful")
    except ValueError:
        print("Invalid ID")


def main() -> None:
    user_operations = {
        1: handle_add_expense,
        2: handle_print_expenses,
        3: handle_filter_by_category,
        4: handle_calculate_total,
        5: handle_calculate_category_total,
        6: handle_delete_expense,
    }

    magic_value = 7

    user_choice = -1

    expenses = storage.load_expenses(FILENAME)

    while user_choice != magic_value:
        print("1. add expense")
        print("2. print expenses")
        print("3. filter expenses by category")
        print("4. calculate expenses total")
        print("5. calculate expenses category total")
        print("6. delete expense")
        print("7. save and exit")

        try:
            user_choice = int(input("Your choice: "))
            if user_choice in user_operations:
                user_operations[user_choice](expenses)
            elif user_choice != magic_value:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")

        print("\n====================================\n")

    storage.save_expenses(expenses, FILENAME)


if __name__ == "__main__":
    main()

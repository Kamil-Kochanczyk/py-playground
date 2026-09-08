import datetime
import decimal
import time
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
        new_expense = Expense(
            expense_id=new_id, amount=new_amount, category=new_category, description=new_description, date=new_date
        )
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
    print(f"Total: {total}")


def handle_calculate_category_total(expenses: list[Expense]) -> None:
    category = Category(input("Category to filter expenses by: "))
    total = operations.calculate_category_total(expenses, category)
    print(f"Category total: {total}")


def handle_delete_expense(expenses: list[Expense]) -> None:
    try:
        id_to_delete = int(input("ID of expense: "))  # type alias not callable so we must use the raw int
        success = operations.delete_expense(expenses, id_to_delete)
        print("Deleted!" if success else "Delete operation unsuccessful")
    except ValueError:
        print("Invalid ID")


def main() -> None:
    time_start = time.perf_counter()

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
            print("Invalid input")
        except decimal.InvalidOperation:
            print("Invalid operation (decimal could not parse a number)")

        print("\n====================================\n")

    storage.save_expenses(expenses, FILENAME)

    time_end = time.perf_counter()

    # time.perf_counter() is for benchmarking, not the "normal" time.time()
    print(f"Session lasted {(time_end - time_start):.3f} s")


if __name__ == "__main__":
    main()

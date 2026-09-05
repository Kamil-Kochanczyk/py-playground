import argparse
import os

from dotenv import load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Loads either true environment variables or their examples."
    )

    parser.add_argument(
        "--example", action="store_true", help="Load .env.example instead of .env"
    )

    args = parser.parse_args()

    filename = ".env.example" if args.example else ".env"

    try:
        load_dotenv(filename)
        print("Environment variables loaded")
    except FileNotFoundError:
        print("File not found")

    login = os.getenv("SECRET_LOGIN")
    key = os.getenv("SECRET_KEY")

    print(f"Login: {login}")
    print(f"Key: {key}")


if __name__ == "__main__":
    # absolute import from the sibling package
    from py_playground.expense_tracker.expense import Expense

    print(Expense.dummy_expense())

    main()

# different configurations - simply change environment variables, the source code remains the same

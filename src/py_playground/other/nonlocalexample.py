import argparse
from collections.abc import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    counter = start

    def inner() -> int:
        nonlocal counter
        counter += 1
        return counter

    return inner


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Set the counter to some value (first argument) and increment it several times (second argument)."
    )

    parser.add_argument("start", type=int, help="Initial counter value")

    parser.add_argument("count", type=int, help="How many times to increment the counter")

    args = parser.parse_args()

    counter = make_counter(args.start)  # e.g. login attempts counter

    for _i in range(args.count):
        print(counter())


if __name__ == "__main__":
    # relative import from the sibling package
    # doesn't work for some reason but it's also not recommended, so no problem
    # from ..expense_tracker import expense
    # print(expense.Expense.dummy_expense())

    # compare what is imported when __all__ is specified inside a module or inside a subpackage
    # from py_playground.other.enumfun import *
    # from py_playground.other import *
    # print(dir())
    # print(Permission.EXEC)

    main()

# Python's scope search order: LEGB = Local - Enclosing - Global - Buil-In

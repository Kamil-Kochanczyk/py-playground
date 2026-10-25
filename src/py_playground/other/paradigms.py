import logging
import random
import string
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypedDict

# imperative: you specify how to achieve the desired result step-by-step (control-flow, e.g. init -> for loop -> append -> print)
# declarative: you specify what result you want to achieve without specyfying how (result, e.g. list comprehension)

# procedural: mostly imperative
# object-oriented: mostly imperative
# functional: mostly declarative

# procedural:
# - relies on mutable state (variables that change) and functions
# - allows creating reusable libraries as packages of functions

# object-oriented:
# - class + instances/objects
# - state (attributes) + behavior (methods)
# - abstraction + encapsulation/hermetisation + inheritance + polymorphism

# functional:
# - relies on evaluation of functions
# - avoids mutable data and changing state
# - map, filter, reduce, recursion, etc.

# procedural and object-oriented paradigms won't be covered here
# only some less known concepts from funtional paradigm will be covered here


# region Example 1 - first-class functions and higher-order functions


# a programming language is said to have first-class functions if it treats functions as first-class citizens
# this means that the language supports passing functions as arguments to other functions,
# returning them as values from other functions,
# and assigning them to variables or storing them in data structures
# a higher-order function is a function that either takes another function as an argument or returns a function


class Order(TypedDict):
    id: int
    total: int


def filter_orders(orders: list[Order], criteria_func: Callable[[Order], bool]) -> list[Order]:
    return [order for order in orders if criteria_func(order)]


# endregion


# region Example 2 - pure functions


# a pure function always returns the exact same output for the same input and has no side effects
# it doesn't modify global variables, alter inputs, or write to databases/files
# this makes code exceptionally easy to test and reason about


def apply_discount(cart_items: list[float], discount_percentage: float) -> list[float]:
    return [item * (1.0 - discount_percentage) for item in cart_items]


# endregion


# region Example 3 - function transformations


# alter or extend existing logic without changing the original source code
# this is how decorators work


class MockAPI(TypedDict):
    id: int
    temp: float
    name: str
    des: str


def description_beautifier(mockapi_fetch_func: Callable[[str], MockAPI]) -> Callable[[str], MockAPI]:
    def beautify(url: str) -> MockAPI:
        fetched_data = mockapi_fetch_func(url)
        fetched_data["des"] = f"{fetched_data['des'].strip().capitalize()}."
        return fetched_data

    return beautify


# @description_beautifier
def mockapi_fetch_func(url: str) -> MockAPI:
    return {
        "id": random.randint(1, 1000),
        "temp": round(random.uniform(-10.0, 40.0), 2),
        "name": f"{url}:{''.join(random.choices(string.ascii_letters + string.digits, k=12))}",
        "des": " ".join(
            "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
            for _ in range(random.randint(3, 8))
        ),
    }


# endregion


# region Example 4 - closures


# a nested function that remembers and retains access to variables in its outer enclosing scope,
# even after the outer function has finished executing
# this lets you encapsulate state without needing classes


def create_id_generator(prefix: str) -> Callable[[], str]:
    counter = -1

    def id_generator() -> str:
        nonlocal counter
        counter += 1
        return f"{prefix}_{counter}"

    return id_generator


# endregion


# region Example 5 - currying


# the process of converting a function that takes multiple arguments into a sequence of functions that each take a single argument


def send_notification(channel: str, recipient: str, message: str) -> str:
    return f"{channel}, {recipient}: {message}"


def send_to_channel(channel: str) -> Callable[[str, str], str]:
    return lambda recipient, message: send_notification(channel, recipient, message)


def send_to_channel_and_recipient(channel: str, recipient: str) -> Callable[[str], str]:
    return lambda message: send_notification(channel, recipient, message)


# endregion


# region Example 6 - sum types


# also known as tagged unions or algebraic data types
# a sum type represents a value that can be one of several different types, but only one at a time
# while common in other languages, Python can model them using Union and pattern matching (match/case)


@dataclass
class Loading: ...


@dataclass
class Success[T]:
    data: T


@dataclass
class IntSuccess(Success[int]): ...


@dataclass
class StrSuccess(Success[str]): ...


@dataclass
class Failure:
    msg: str


type FetchSuccess = IntSuccess | StrSuccess


type State = Loading | FetchSuccess | Failure


def render_ui(logger: logging.Logger, state: State) -> None:
    match state:
        case Loading():
            logger.info("Loading...")
        case IntSuccess(data=value):
            logger.info("Success with int: %d", value)
        case StrSuccess(data=value):
            logger.info("Success with str: %s", value)
        case Failure(msg=message):
            logger.warning("Failure, %s", message)
        case _:
            raise AssertionError("The default case executed")


# endregion


def main() -> None:
    logging.basicConfig(format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%H:%M:%S")
    logger = logging.getLogger("Paradigms")
    logger.setLevel(logging.INFO)

    orders: list[Order] = [{"id": 1, "total": 50}, {"id": 2, "total": 150}, {"id": 3, "total": 20}]
    magic_value = 100
    logger.info(filter_orders(orders, lambda order: order["total"] < magic_value))

    cart_items = [10.86, 42.69, 0.25]
    discount_percentage = 0.03
    logger.info(apply_discount(cart_items, discount_percentage))
    logger.info(cart_items)

    logger.info("NORMAL:")
    fetched1 = [mockapi_fetch_func(f"url{i}") for i in range(5)]
    for data in fetched1:
        logger.info(data)

    logger.info("NORMAL + DESCRIPTION BEAUTIFIER:")
    fetched2 = [description_beautifier(mockapi_fetch_func)(f"url{i}") for i in range(5)]
    for data in fetched2:
        logger.info(data)

    id_generator = create_id_generator("IDGEN")
    for _ in range(5):
        logger.info(id_generator())

    emails = ["alice@gmail.com", "bob@gmail.com"]
    recipients = ["Alice", "Bob"]

    logger.info("FIXED EMAIL:")
    for i, email in enumerate(emails):
        email_notifier = send_to_channel(email)

        for j, recipient in enumerate(recipients):
            logger.info(email_notifier(recipient, f"msg_{i}_{j}"))

    logger.info("FIXED EMAIL AND RECIPIENT:")
    for i, email in enumerate(emails):
        for j, recipient in enumerate(recipients):
            email_recipient_notifier = send_to_channel_and_recipient(email, recipient)
            logger.info(email_recipient_notifier(f"msg_{i}_{j}"))

    loading_obj = Loading()
    int_success_obj = IntSuccess(10)
    str_success_obj = StrSuccess("cinos")
    failure_obj = Failure("you are a terrible loser")
    objs: list[State] = [loading_obj, int_success_obj, str_success_obj, failure_obj]
    for obj in objs:
        render_ui(logger, obj)


if __name__ == "__main__":
    main()

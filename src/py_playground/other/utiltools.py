import random
import time
from collections import Counter, defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache, wraps
from itertools import accumulate, chain, combinations, count, cycle, groupby, islice, permutations, product, repeat
from typing import Any, Literal

from rich import print as rprint

type Country = Literal["Poland", "Spain", "France"]


@dataclass
class User:
    user_id: int
    country: Country


@lru_cache(maxsize=512)
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n in {0, 1}:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def bad_decorator[F: Callable[..., Any]](func: F) -> F:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        rprint("Pretty print")
        func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


@bad_decorator
def bad_greet(name: str) -> None:
    """Greet the user with minion's greeting (bad).

    Args:
        name (str): name of the user to greet (bad)

    """
    rprint(f"Bello {name}!")


def good_decorator[F: Callable[..., Any]](func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        rprint("Pretty print")
        func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


@good_decorator
def good_greet(name: str) -> None:
    """Greet the user with minion's greeting (good).

    Args:
        name (str): name of the user to greet (good)

    """
    rprint(f"Bello {name}!")


def collections_examples() -> None:
    letters_counter = Counter("abrakadabra")
    rprint(letters_counter)
    rprint(letters_counter["a"])

    words_counter = Counter(["cat", "dog", "cat", "bird", "dog", "cat"])
    rprint(words_counter)
    rprint(words_counter.most_common(2))

    groups = defaultdict(list)  # create an empty list when a key doesn't exist yet and is accessed for the first time
    groups["A"].append("aaa")
    groups["A"].append("aaa")
    groups["B"].append("bbb")
    rprint(groups)
    rprint(groups["C"])
    rprint(groups)

    scores = defaultdict(int)  # type: ignore[]
    scores["Me"] += 100
    scores["You"] -= 100
    rprint(scores)  # creates 0 for default

    double_ended = deque([1, 2, 3])
    double_ended.append(4)
    double_ended.appendleft(0)
    rprint(double_ended)
    double_ended.pop()
    double_ended.popleft()
    rprint(double_ended)
    rprint(len(double_ended))


def itertools_examples() -> None:

    # infinite sequences
    my_id_limit = 50
    for my_id in count(1, 10):
        rprint(my_id)
        if my_id > my_id_limit:
            break

    # lazily chain lists, without creating one giant list
    for value in chain([1, 2], [3, 4], [5, 6]):
        rprint(value)

    # slice an iterator as if it were an iterable
    for number in islice(count(), 10):
        rprint(number)

    # cartesian product
    for x, y in product(range(3), range(3)):
        rprint(f"{x}, {y}")

    # combinations
    for b1, b2, b3 in combinations(["star1", "star2", "star3", "star4", "star5"], 3):
        rprint(f"Three-body problem: {b1}, {b2}, {b3}")
    rprint(len(list(combinations(["star1", "star2", "star3", "star4", "star5"], 3))))

    # permutations
    for perm in permutations(["a", "b", "c", "d"], 3):
        rprint(perm)
    rprint(len(list(permutations(["a", "b", "c", "d"], 3))))

    # accumulation
    for damage in accumulate([10, 25, 100]):
        rprint(damage)

    # cycling
    dirs = ["N", "S", "E", "W"]
    dir_counter = Counter(dict.fromkeys(dirs, 0))
    max_iters = 3
    for d in cycle(dirs):
        rprint(d)
        dir_counter[d] += 1
        rprint(dir_counter)
        if dir_counter[d] > max_iters:
            break

    # group by a key
    id_generator = count()
    countries: list[Country] = ["Poland", "Spain", "France"]
    users = [User(next(id_generator), random.choice(countries)) for _ in range(10)]
    rprint(users)
    users_sorted = sorted(users, key=lambda user: user.country)  # groupby should always operate on sorted iterables
    rprint(users_sorted)
    for country, group in groupby(users_sorted, key=lambda user: user.country):
        rprint(f"{country}: {list(group)}")

    # repeat yielding the same object over and over again
    for user, greeting in zip(users_sorted, repeat("Bello!", len(users_sorted)), strict=True):
        rprint(f"{greeting} {user.user_id}")


def functools_examples() -> None:
    # remove the lru_cache decorator to see the performance impact
    start = time.perf_counter()
    rprint(f"fibonacci(100) = {fibonacci(42)}")
    end = time.perf_counter()
    rprint(f"Time: {end - start} s")
    rprint(f"Cache statistic: {fibonacci.cache_info()}")

    # lost metadata
    bad_greet("Kamil")
    rprint(bad_greet.__name__)
    rprint(bad_greet.__doc__)

    # preserved metadata
    good_greet("Kamil")
    rprint(good_greet.__name__)
    rprint(good_greet.__doc__)


def main() -> None:
    collections_examples()
    rprint()
    itertools_examples()
    rprint()
    functools_examples()


if __name__ == "__main__":
    main()

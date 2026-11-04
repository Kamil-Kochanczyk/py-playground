import sys

# lazy from json import dumps
lazy import json

from rich import print as rprint
from rich.traceback import install

install()

# sentinel value is used to denote a missing value
# in some cases None can be used to denote a missing value but not always
# when None is a meaningful value, then you can't differentiate between "None as a meaningful value" vs "None as a lack of value"
# note: module-level sentinel value allows the "is MISSING" check to work even in different subprocesses
MISSING = sentinel("MISSING")


def compare_none_and_sentinel(somearg: str | sentinel | None = MISSING) -> None:
    if somearg is MISSING:
        raise KeyError("Missing argument detected")
    if somearg is None:
        rprint("None is a meaningful value here")


def main() -> None:
    rprint(f"sys loaded: {'sys' in sys.modules}")
    rprint(f"json loaded: {'json' in sys.modules}")
    rprint(json.dumps({"theme": "dark", "autosave": True}))
    rprint(f"json loaded: {'json' in sys.modules}")

    # nested_lists = [[1, 2], [3, 4], [[5, 6], [7, 8]]]
    # rprint(nested_lists)
    # rprint([*flattened for flattened in nested_lists])
    # layers = [{"port": 8080, "pswd": "***"}, {"port": 5432}, {"debug": True}]
    # rprint(layers)
    # rprint({**layer for layer in layers})

    # reminder:
    # - immutable vs mutable types in Python
    # - hashable vs unhashable types in Python
    # - bonus: relationship between hashability and equality
    # --- equal objects must have the same hash (correct look-up in dicts or sets)
    # --- unequal objects may happen to have the same hash (hash collisions, should be as rare as possible)
    # --- if equality logic changes, hashing logic should match the equality logic
    # --- usually, object properties used for equality comparison should also be used to calculate the hash of the object
    # --- otherwise equal objects might happen to have different hashes
    # - the golden rule: only immutable objects should be hashable (otherwise object may change its hash and screw up dict/set lookup)
    # - hash function:
    # --- calculates a number in contant-time
    # --- the number represents a bucket in a hash table
    # --- therefore, hash function mapps an object to a bucket, i.e. a slot in an array where the data is stored
    # - two ways to implement a hash table: separate chaining vs open addressing
    # --- separate chaining stores linked lists in an array, those linked lists are buckets where lookup takes place, if collision, then append to linked list
    # --- open addressing stores elements in an array, if collision, then look for a free spot in the array (e.g. if N taken, then check N+1, then check N+2, ...)
    # - dicts and sets use hashes for contant-time, fast lookup
    # - dicts use keys for value lookups, sets use their elements to check if they are already registered in the set
    # - therefore, only immutable types are allowed as dict keys or as set elements
    # - dicts and sets are mutable
    # - frozendicts and frozensets are immutable

    fav_nums_set = frozenset([42, 69, 520])
    # fav_nums_set = {42, 69, 520}
    # fav_nums_set.add(10)
    rprint(fav_nums_set, hash(fav_nums_set))

    config = frozendict({"theme": "dark", "autosave": True})
    # config = {"theme": "dark", "autosave": True}
    # config["theme"] = "system"
    rprint(config | {"theme": "light", "port": 8000}, hash(config), isinstance(config, dict))

    rprint(MISSING, type(MISSING))
    # compare_none_and_sentinel()
    compare_none_and_sentinel(None)


if __name__ == "__main__":
    main()

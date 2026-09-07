# Basics

This cheatsheet is mainly based on mypy documentation.

```python
# This is how you declare the type of a variable
age: int = 1

# You don't need to initialize a variable to annotate it
a: int  # Ok (no value at runtime until assigned)

# Doing so can be useful in conditional branches
child: bool
if age < 18:
    child = True
else:
    child = False
```

```python
# For most types, just use the name of the type in the annotation
# Note that mypy can usually infer the type of a variable from its value,
# so technically these annotations are redundant
x: int = 1
x: float = 1.0
x: bool = True
x: str = "test"
x: bytes = b"test"

# For collections, the type of the collection item is in brackets
x: list[int] = [1]
x: set[int] = {6, 7}

# For mappings, we need the types of both keys and values
x: dict[str, float] = {"field": 2.0}

# For tuples of fixed size, we specify the types of all the elements
x: tuple[int, str, float] = (3, "yes", 7.5)

# For tuples of variable size, we use one type and ellipsis
x: tuple[int, ...] = (1, 2, 3)

# On Python 3.8 and earlier, the name of the collection type is
# capitalized, and the type is imported from the 'typing' module
from typing import List, Set, Dict, Tuple
x: List[int] = [1]
x: Set[int] = {6, 7}
x: Dict[str, float] = {"field": 2.0}
x: Tuple[int, str, float] = (3, "yes", 7.5)
x: Tuple[int, ...] = (1, 2, 3)

from typing import Union, Optional

# Use the | operator when something could be one of a few types
x: list[int | str] = [3, 5, "test", "fun"]
# Union is equivalent
x: list[Union[int, str]] = [3, 5, "test", "fun"]

# Use X | None for a value that could be None; Optional[X] is the same as X | None
x: str | None = "something" if some_condition() else None
if x is not None:
    # Mypy understands x won't be None here because of the if-statement
    print(x.upper())
# If you know a value can never be None due to some logic that mypy doesn't
# understand, use an assert
assert x is not None
print(x.upper())
```

```python
from collections.abc import Iterator, Callable
from typing import Union, Optional

# This is how you annotate a function definition
def stringify(num: int) -> str:
    return str(num)

# And here's how you specify multiple arguments
def plus(num1: int, num2: int) -> int:
    return num1 + num2

# If a function does not return a value, use None as the return type
# Default value for an argument goes after the type annotation
def show(value: str, excitement: int = 10) -> None:
    print(value + "!" * excitement)

# Note that arguments without a type are dynamically typed (treated as Any)
# and that functions without any annotations are not checked
def untyped(x):
    x.anything() + 1 + "string"  # no errors

# This is how you annotate a callable (function) value
x: Callable[[int, float], float] = f
def register(callback: Callable[[str], int]) -> None: ...

# A generator function that yields ints is secretly just a function that
# returns an iterator of ints, so that's how we annotate it
def gen(n: int) -> Iterator[int]:
    i = 0
    while i < n:
        yield i
        i += 1

# You can of course split a function annotation over multiple lines
def send_email(
    address: str | list[str],
    sender: str,
    cc: list[str] | None,
    bcc: list[str] | None,
    subject: str = '',
    body: list[str] | None = None,
) -> bool:
    ...

# Mypy understands positional-only and keyword-only arguments
# Positional-only arguments can also be marked by using a name starting with
# two underscores
def quux(x: int, /, *, y: int) -> None:
    pass

quux(3, y=5)  # Ok
quux(3, 5)  # error: Too many positional arguments for "quux"
quux(x=3, y=5)  # error: Unexpected keyword argument "x" for "quux"

# This says each positional arg and each keyword arg is a "str"
def call(self, *args: str, **kwargs: str) -> str:
    reveal_type(args)  # Revealed type is "tuple[str, ...]"
    reveal_type(kwargs)  # Revealed type is "dict[str, str]"
    request = make_request(*args, **kwargs)
    return self.do_api_query(request)
```

```python
from typing import ClassVar

class BankAccount:
    # The "__init__" method doesn't return anything, so it gets return
    # type "None" just like any other method that doesn't return anything
    def __init__(self, account_name: str, initial_balance: int = 0) -> None:
        # mypy will infer the correct types for these instance variables
        # based on the types of the parameters.
        self.account_name = account_name
        self.balance = initial_balance

    # For instance methods, omit type for "self"
    def deposit(self, amount: int) -> None:
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        self.balance -= amount

# User-defined classes are valid as types in annotations
account: BankAccount = BankAccount("Alice", 400)
def transfer(src: BankAccount, dst: BankAccount, amount: int) -> None:
    src.withdraw(amount)
    dst.deposit(amount)

# Functions that accept BankAccount also accept any subclass of BankAccount!
class AuditedBankAccount(BankAccount):
    # You can optionally declare instance variables in the class body
    audit_log: list[str]

    def __init__(self, account_name: str, initial_balance: int = 0) -> None:
        super().__init__(account_name, initial_balance)
        self.audit_log: list[str] = []

    def deposit(self, amount: int) -> None:
        self.audit_log.append(f"Deposited {amount}")
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        self.audit_log.append(f"Withdrew {amount}")
        self.balance -= amount

audited = AuditedBankAccount("Bob", 300)
transfer(audited, account, 100)  # type checks!

# You can use the ClassVar annotation to declare a class variable
class Car:
    seats: ClassVar[int] = 4
    passengers: ClassVar[list[str]]
```

```python
from typing import Union, Any, Optional, TYPE_CHECKING, cast

# To find out what type mypy infers for an expression anywhere in
# your program, wrap it in reveal_type().  Mypy will print an error
# message with the type; remove it again before running the code.
reveal_type(1)  # Revealed type is "builtins.int"

# If you initialize a variable with an empty container or "None"
# you may have to help mypy a bit by providing an explicit type annotation
x: list[str] = []
x: str | None = None

# Use Any if you don't know the type of something or it's too
# dynamic to write a type for
x: Any = mystery_function()
# Mypy will let you do anything with x!
x.whatever() * x["you"] + x("want") - any(x) and all(x) is super  # no errors

# Use a "type: ignore" comment to suppress errors on a given line,
# when your code confuses mypy or runs into an outright bug in mypy.
# Good practice is to add a comment explaining the issue.
x = confusing_function()  # type: ignore  # confusing_function won't return None here because ...

# "cast" is a helper function that lets you override the inferred
# type of an expression. It's only for mypy -- there's no runtime check.
a = [4]
b = cast(list[int], a)  # Passes fine
c = cast(list[str], a)  # Passes fine despite being a lie (no runtime check)
reveal_type(c)  # Revealed type is "builtins.list[builtins.str]"
print(c)  # Still prints [4] ... the object is not changed or casted at runtime

# Use "TYPE_CHECKING" if you want to have code that mypy can see but will not
# be executed at runtime (or to have code that mypy can't see)
if TYPE_CHECKING:
    import json
else:
    import orjson as json  # mypy is unaware of this
```

```python
from collections.abc import Mapping, MutableMapping, Sequence, Iterable
# or 'from typing import ...' (required in Python 3.8)

# Use Iterable for generic iterables (anything usable in "for"),
# and Sequence where a sequence (supporting "__len__" and "__getitem__") is
# required

def f(ints: Iterable[int]) -> list[str]:
    return [str(x) for x in ints]

f(range(1, 3))

def g(seq: Sequence[int]) -> tuple[int, int]:
    return seq[0], len(seq)

g([1, 2, 3])
```

```python
# You may want to reference a class before it is defined.
# This is known as a "forward reference".
def f(foo: A) -> int:  # This will fail at runtime with 'A' is not defined
    ...

# However, if you add the following special import:
from __future__ import annotations
# It will work at runtime and type checking will succeed as long as there
# is a class of that name later on in the file
def f(foo: A) -> int:  # Ok
    ...

# Another option is to just put the type in quotes
def f(foo: 'A') -> int:  # Also ok
    ...

class A:
    # This can also come up if you need to reference a class in a type
    # annotation inside the definition of that class
    @classmethod
    def create(cls) -> A:
        ...
```

```python
from collections.abc import Callable
from typing import Any

# 1. BARE DECORATOR
# Usage: @bare_decorator
def bare_decorator[F: Callable[..., Any]](func: F) -> F:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print("Executing bare decorator log...")
        return func(*args, **kwargs)
    
    # Return wrapper cast/treated as type F
    return wrapper  # type: ignore[return-value]


# 2. DECORATOR WITH ARGUMENTS
# Usage: @decorator_args(url="https://api.example.com")
def decorator_args[F: Callable[..., Any]](url: str) -> Callable[[F], F]:
    def actual_decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"Calling endpoint: {url}")
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore[return-value]
        
    return actual_decorator


# --- HOW THEY ARE USED ---

@bare_decorator
def add(a: int, b: int) -> int:
    return a + b

@decorator_args(url="https://api.example.com/data")
def fetch_user(user_id: int) -> str:
    return f"User_{user_id}"


# The type checker preserves exact function signatures:
result_add = add(5, 10)         # Type checker knows result_add is an 'int'
result_user = fetch_user(42)    # Type checker knows result_user is a 'str'
```

# Notes

- **MyPy** is a static type checker
- static type checking if just for more accurate workflow and for making the code more understandable and manageable, it has no effect on the runtime behaviour, e.g. errors given by mypy do not prevent from running the script, it also cannot ensure that the data coming from external sources is in the correct form (this is the task of runtime validation, not static type checking)
- `...` is called the **Ellipsis** and it's used in:
  - numpy, indicating the full slice `[:]` for all the dimensions in the gap it is placed, so for a 3d array, `a[..., 0]` is the same as `a[:, :, 0]` and for 4d `a[:, :, :, 0]`, similarly, `a[0, ..., 0]` is `a[0, :, :, 0]` (with however many colons in the middle make up the full number of dimensions in the array)
  - the same situations as the `pass` keyword
  - typing, where it specifies a callable that returns something but has no known param signature (e.g. `Callable[..., int]`) or a tuple of variable size (e.g. `tuple[int, ...]`)
- `object` is the base class of Python, anything in Python can be treated as `object`, `object` can be checked by a type checker, e.g. every checker will be satisfied with `obj: object; print(obj)` because every object can be printed, but no one will be satisfied with `obj: object; obj.foo()` because not every Python object has a method `foo()` defined
- `Any` is not the same as `object`, it is not checked by the type checker (when it sees `Any`, it assumes that it can be anything), it is preferred to use `object` when you do not know what type you are expecting or when you do not care
- function's param list can be broken into three distinct zones
  - `def example(positional_only, /, standard, *, keyword_only):`
  - everything before `/` must be passed as a positional argument (e.g., `3`), you cannot use its name (e.g., `x=3`)
  - everything after `*` must be passed as a keyword argument (e.g., `y=5`), you cannot pass it by position alone (e.g., `5`)
  - anything between `/` and `*` can be passed either way
- if you have a class variable (variable defined inside a class, not inside one of the methods in the class), this variable is shared across all instances of the class, but when you try to access it through an instance (e.g. `instance_name.variable_name` instead of `ClassName.variable_name`), this instance gets its own version of the accessed variable which shadows the original class variable and is a completely independent variable from now on
- things get more messy when you use type annotations, it seems that when you add a type annotation to a variable defined inside class body, Python actually does not see it as a class variable and does not create any variable whatsoever, instead such annotated variable is simply an information to a type checker about the type this variable should have when attached to `self` later in the code (to actually annotate a class variable you have to use `ClassVar` instead)
- **duck typing** is the philosophy of Python, it means you don't care what class the object belongs to or what parent class it inherits from, you simply assume the object can perform the operation and try to call it, e.g. Python does not care if in `obj.fly()` the `obj` has the right type, the only thing it cares about is if the `obj` has the `fly()` method
- `Iterable` is an object wich can be iterated in the `for` loop, it is defined by `__iter__` or `__getitem__` method
- `Sequence` is an object which has elements assigned to positions (indices, starting from `0`), it is defined by `__len__` and `__getitem__` methods, supports the following operations: `seq[0]`, `seq[0:1:2]`, `sth in seq`, `len(seq)`, `seq.count()`, `for item in seq`
- sometimes third-party libraries don't have enough type information to satisfy type checkers, for such libraries people often create their separate versions which contain no runtime code whatsoever but only the information about the types, we call such files **stub files**
- **stub files** in Python (`.pyi` files) contain type hint information for Python modules without any operational runtime code, they allow type checkers like mypy to perform static type analysis on dynamically written Python (they can also be used for modules written in C/C++), a typical structure of a `.pyi` file directly mirrors its `.py` counterpart but replaces the actual implementations with `...` (**Ellipsis**)
- **Pydantic** is a runtime data validation library, it is useful when you expect the data to have a particular structure but you have no guarante that it will satisfy this structure because it e.g. comes from an external, unpredictable source that does not guarantee data correctness, etc.
- **Pydantic** lets you describe the structure of your data using Python types and then validate data against that structure, it doesn't merely check types, by default it can also parse/coerce compatible input into the declared types unless the input is completely incompatible with the declared types
- you can use **Pydantic** to check if your data is valid, to transform data into the shapes you need, and then serialize the results so they can be moved on to other applications

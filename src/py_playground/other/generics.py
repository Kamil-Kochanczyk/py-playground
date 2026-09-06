from typing import Any, ClassVar, Final, Literal, Protocol


# type constraint - tuple of allowed types (T can be "one of these")
def swap_immutable[T: (int, str)](a: T, b: T) -> None:
    b, a = a, b


# type bound - upper limit for allowed types (T can be "this or any subclass/subtype of this")
def swap_mutable[T: list[Any]](a: T, b: T) -> None:
    b, a = a, b


# generic classes - because why not?
class Node[T: int | str]:
    def __init__(self, value: T) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"


class Sonic:
    name: ClassVar[str] = "Sonic"

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        print("Run Sonic!")


class Shadow:
    name: ClassVar[str] = "Shadow"

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        print("Run Shadow!")


# the following is not really generics but still good to know


# protocol defines a special type acting like a common interface for related types
# kind-of like abstract base class
# it is just for type checkers
class CoolHedgehog(Protocol):
    def run(self) -> None: ...


def make_run(someone: CoolHedgehog) -> None:
    someone.run()


type HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]


def go_http(method: HttpMethod) -> None:
    print(method)


# other useful constructs: @override, @overload


def main() -> None:
    c: int = 10
    d: int = 8
    swap_immutable(c, d)
    print(f"c = {c}; d = {d}")

    e: list[int] = [10]
    f: list[int] = [8]
    swap_mutable(e, f)
    print(f"e = {e}; f = {f}")

    n = Node("2.0")
    print(str(n))

    make_run(Sonic())
    make_run(Shadow())

    go_http("GET")  # only one of four specified values will satisfy the type checker

    m: Final = 0  # type checker knows that this value shouldn't be changed later
    # m = 1
    print(m)


if __name__ == "__main__":
    main()

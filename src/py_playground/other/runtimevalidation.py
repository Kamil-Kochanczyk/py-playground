from __future__ import annotations

from abc import abstractmethod
from dataclasses import asdict, astuple, dataclass, field
from random import randint
from typing import (
    Annotated,
    Any,
    NamedTuple,
    Protocol,
    Self,
    TypeVar,
    get_args,
    get_type_hints,
)

from pydantic import (
    AfterValidator,
    AliasChoices,
    AliasGenerator,
    AliasPath,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
    model_validator,
)

# add metadata without changing the interpretation of static type checkers
# metadata can be used at runtime for example to enforce validation
Speed = Annotated[float, "m/s"]
Distance = Annotated[float, "m"]
Time = Annotated[float, "s", {"min": 0}]


def check_speed(v: Speed, s: Distance, t: Time) -> bool:
    if t != 0:
        return v == s / t
    raise ZeroDivisionError("Time cannot be 0")


# protocol for anything comparable
class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: CT, other: CT, /) -> bool: ...


CT = TypeVar("CT", bound=Comparable)


# dataclass is a decorator which creates many dunder methods automatically for you
# useful if a class is mainly used as a container for related data rather than for having some functionality
# type hints required
# fields with default values must follow fields without default values
# field() is for more complex default values
# mutable types in particular should never be assigned as default values directly but only inside field()
# otherwise all dataclass instances will share the same list/dict/etc.
# freezing a dataclass emulates its immutability
@dataclass(frozen=True)
class Top3[CT]:
    first: CT
    second: CT
    third: CT
    honorable_mentions: list[CT] = field(default_factory=list)


# another container for related values is NamedTuple
# it is just a tuple (immutable tuple) but it additionaly gives you access to obj.property syntax
# it even allows you to define custom properties and methods
class WhatIsIt(NamedTuple):
    goh: str
    hoh: str
    dl: str

    def concat(self) -> str:
        return f"{self.goh}; {self.hoh}; {self.dl}"


# Pydantic has two contexts when it comes to interpreting "Before" and "After" validators: field context and model context
# in field context you validate a single field of an instance
# in model context you validate multiple fields to ensure their mutual relationship are as desired
# in field context "Before" means "before default validation" and "After" means "after default validation"
# in model context "Before" means "before instance initialization" and "After" means "after instance initialization"
# default (internal) validation is the automatic validaton done by Pydantic when the instance is created and types are checked/parsed/etc.
# "Before" also allows you to transform the data while still having it in its raw form
# you can specify field validators in two ways: using Annotated and using decorators
# model validators are specified using decarators
# note: in Pydantic, just like in dataclasses,
# it is a good practice to use Field() and default_factory for default values of mutable types, e.g. list/dict,
# even though Pydantic helps you and creates a deepcopy if you use a mutable type as a default value of some attribute


class Validators:
    # not that "Before" deals with raw values, hence "Any"
    # "After" deals with validated values so "Any" can be replaced with sth more specific
    @staticmethod
    def clean_entity_name(value: Any) -> str:
        if isinstance(value, str):
            return value.lower().strip()
        raise ValueError("Entity name is not a string :(")


class Entity(BaseModel):
    model_config = ConfigDict()

    entity_id: Annotated[int, Field(ge=0)]

    # region field-level validation (Annotated way)
    # change the mode from "Before" to "After" to see if "Ranking   " passes the validation
    name: Annotated[
        str,
        Field(min_length=1, max_length=7),
        BeforeValidator(Validators.clean_entity_name),
    ]
    # name: Annotated[
    #     str,
    #     Field(min_length=1, max_length=7),
    #     AfterValidator(Validators.clean_entity_name),
    # ]
    # endregion

    # region field-level validation (decorators way)
    # name: Annotated[str, Field(min_length=1, max_length=7)]
    # @field_validator("name", mode="before")
    # @field_validator("name", mode="after")
    # @classmethod
    # def clean_my_name(cls, value: Any) -> str:
    #     if isinstance(value, str):
    #         return value.upper().strip()
    #     raise ValueError("Entity name is not a string :(")
    # endregion

    description: str | None = None
    category: str | None = None

    # region model-level validation
    @model_validator(mode="before")
    @classmethod
    def ensure_not_too_long(cls, data: Any) -> Any:
        magic_value = 7
        if (
            isinstance(data, dict)
            and ("description" in data)
            and (isinstance(data["description"], str))
            and (len(data["description"]) > magic_value)
        ):
            raise ValueError("Too long description >;p")
        if (
            isinstance(data, dict)
            and ("category" in data)
            and (isinstance(data["category"], str))
            and (len(data["category"]) > magic_value)
        ):
            raise ValueError("Too long category >;p")
        return data

    @model_validator(mode="after")
    def ensure_non_empty(self) -> Self:
        if isinstance(self.description, str) and len(self.description) == 0:
            raise ValueError("Empty description >:(")
        if isinstance(self.category, str) and len(self.category) == 0:
            raise ValueError("Empty category >:(")
        return self

    # endregion


class Relationship(BaseModel):
    model_config = ConfigDict()

    relationship_id: Annotated[int, Field(ge=0)]
    src: Entity
    dst: Entity
    name: Annotated[str, Field(min_length=1, max_length=30)]


class AliasGenerators:
    @staticmethod
    def get_user_validation_aliases() -> dict[str, AliasChoices]:
        return {
            "email": AliasChoices("e-mail", "E-mail", "E-Mail", "Email", AliasPath("other", 0)),
            "key": AliasChoices(
                "Key",
                "password",
                "Password",
                "pwd",
                "Pwd",
                "PWD",
                AliasPath("other", 1),
            ),
        }

    @staticmethod
    def get_user_serialization_aliases() -> dict[str, list[str]]:
        return {
            "email": ["e-mail", "E-mail", "E-Mail", "Email"],
            "key": ["Key", "password", "Password", "pwd", "Pwd", "PWD"],
        }


class User(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
        alias_generator=AliasGenerator(
            # verify against the predefined aliases
            validation_alias=lambda field_name_str: AliasGenerators.get_user_validation_aliases().get(
                field_name_str, field_name_str
            ),
            # choose randomly from predefined aliases
            serialization_alias=lambda field_name_str: (
                AliasGenerators.get_user_serialization_aliases()[field_name_str][
                    randint(
                        0,
                        len(AliasGenerators.get_user_serialization_aliases()[field_name_str]) - 1,
                    )
                ]
                if field_name_str in AliasGenerators.get_user_serialization_aliases()
                else field_name_str
            ),
        ),
    )

    # alias is an alternative name
    # alias param is used for both validation and serialization
    # other params: validation_alias, serialization_alias
    name: Annotated[str, Field(min_length=1, alias="username")]

    email: EmailStr
    key: SecretStr


def main() -> None:
    # Annotate
    print(check_speed(1.0, 4.0, 2.0))
    print(get_args(Time), get_args(Time)[0], get_args(Time)[1:])
    print(get_type_hints(check_speed, include_extras=True))
    print()

    # dataclass
    favourite_numbers = Top3(10, 8, 5, [42, 69, 520])
    # favourite_numbers.third = 6  # this assignment is caught as an error
    # favourite_numbers.honorable_mentions[0] = 6  # but this assignment is not caught
    print(favourite_numbers)  # __repr__ automaticallly defined
    print(
        max(favourite_numbers.honorable_mentions),
        min(favourite_numbers.honorable_mentions),
    )
    print(asdict(favourite_numbers))
    print(astuple(favourite_numbers))
    print()

    # NamedTuple
    whatisit = WhatIsIt("Done!", "Almost done!", "Long way to be done!")
    print(whatisit.goh, whatisit.hoh, whatisit.dl)
    print(whatisit.concat())
    print()

    # Pydantic

    # ranking = Entity(entity_id=-1, name="")
    ranking = Entity(entity_id=0, name="Ranking   ")
    print(ranking)

    data = {"entity_id": "10", "name": "pypy"}
    data_json = '{"entity_id": "10", "name": "pypy_j"}'

    pypy = Entity.model_validate(data)
    print(pypy, pypy.name, pypy.model_dump())
    pypy_json = Entity.model_validate_json(data_json)
    print(pypy_json, pypy_json.name, pypy_json.model_dump_json())
    print()

    similar = Relationship(
        relationship_id=0,
        src=pypy,
        dst=pypy_json,
        name="Confusingly similar",
    )
    print(similar.model_json_schema())
    print()

    user = User(username="Kamil", email="kamil@gmail.com", key=SecretStr("limaK"))  # type: ignore[]  # mypy doesn't understand pydantic's alias :(
    print(user, user.model_dump(), user.model_dump_json())
    print(user.key.get_secret_value())

    # user_data = {
    #     "username": "Aliased",
    #     "E-mail": "aliased@aliased.com",
    #     "PWD": "desailA",
    # }
    user_data = {"username": "Aliased", "other": ["aliased@aliased.com", "desailA"]}
    aliased_user = User.model_validate(user_data, by_alias=True)
    print(aliased_user.model_dump_json(by_alias=True))


if __name__ == "__main__":
    main()

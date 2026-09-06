from __future__ import annotations

import datetime
import decimal
from typing import TypedDict


class Expense:
    def __init__(
        self,
        expense_id: int,
        amount: decimal.Decimal,
        category: str,
        description: str,
        date: datetime.datetime,
    ) -> None:
        self.id = expense_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def _members(self) -> tuple[int, decimal.Decimal, str, str, datetime.datetime]:
        return (self.id, self.amount, self.category, self.description, self.date)

    def __eq__(self, other: object) -> bool:
        # __hash__ implicitly set to None because we don't define it
        # we don't define __hash__ because Expense is mutable
        # comparing types like below restrictive
        # for example, it doesn't consider parent class and child classes to be of the same type
        if type(self) is type(other):
            return self._members() == other._members()
        return False

    @classmethod
    def dummy_expense(
        cls,
        expense_id: int = 0,
        amount: decimal.Decimal = decimal.Decimal("0.0"),
        category: str = "",
        description: str = "",
        date: datetime.datetime | None = None,
    ) -> Expense:
        if date is None:
            date = datetime.datetime.min.replace(tzinfo=datetime.UTC)

        return cls(
            expense_id,
            amount,
            category,
            description,
            date,
        )


class ExpenseDict(TypedDict):
    id: int
    amount: str
    category: str
    description: str
    date: str

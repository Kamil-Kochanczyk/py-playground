from __future__ import annotations

import datetime
import decimal
from typing import NewType, NotRequired, TypedDict

from pydantic import BaseModel

type ExpenseID = int  # type alias, i.e. giving another name for readability purposes

# new types, similar to type aliases
# used to differentiate between conceptually different values of the same type
Category = NewType("Category", str)
Description = NewType("Description", str)


class Expense(BaseModel):
    expense_id: ExpenseID
    amount: decimal.Decimal
    category: Category
    description: Description
    date: datetime.datetime

    def _members(
        self,
    ) -> tuple[ExpenseID, decimal.Decimal, Category, Description, datetime.datetime]:
        return (self.expense_id, self.amount, self.category, self.description, self.date)

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
        exp_id: ExpenseID = 0,
        amt: decimal.Decimal = decimal.Decimal("0.0"),
        cat: Category = Category(""),
        des: Description = Description(""),
        dattim: datetime.datetime | None = None,
    ) -> Expense:
        if dattim is None:
            dattim = datetime.datetime.min.replace(tzinfo=datetime.UTC)

        return cls(
            expense_id=exp_id,
            amount=amt,
            category=cat,
            description=des,
            date=dattim,
        )


class ExpenseDict(TypedDict):
    id: ExpenseID
    amount: str
    category: Category
    description: Description
    date: str
    receiver: NotRequired[str]

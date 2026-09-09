"""Expense data models and helpers for the expense tracker."""

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
    """Represents a single expense entry.

    Attributes:
        expense_id: Unique identifier for the expense.
        amount: Monetary value of the expense.
        category: Expense category label.
        description: Free-form description of the expense.
        date: Timestamp when the expense occurred.

    """

    expense_id: ExpenseID
    amount: decimal.Decimal
    category: Category
    description: Description
    date: datetime.datetime

    def _members(
        self,
    ) -> tuple[ExpenseID, decimal.Decimal, Category, Description, datetime.datetime]:
        """Return the fields used to compare two expense instances.

        Returns:
            A tuple containing the fields that define the expense identity and values.

        """
        return (self.expense_id, self.amount, self.category, self.description, self.date)

    def __eq__(self, other: object) -> bool:
        """Check whether another object is an equivalent Expense instance.

        Args:
            other: The object to compare against.

        Returns:
            True if `other` is an Expense with identical field values; otherwise False.

        """
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
        """Create a placeholder Expense instance with default values.

        Args:
            exp_id: Identifier to assign to the dummy expense.
            amt: Amount to store on the dummy expense.
            cat: Category to store on the dummy expense.
            des: Description to store on the dummy expense.
            dattim: Optional explicit date for the dummy expense. When omitted,
                the minimum UTC datetime is used.

        Returns:
            A new Expense instance populated with the supplied values.

        """
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
    """Typed dictionary representation of an expense for JSON serialization.

    Attributes:
        id: Expense identifier.
        amount: Stringified monetary amount.
        category: Expense category.
        description: Expense description.
        date: ISO-formatted expense date string.
        receiver: Optional receiver information for the expense.

    """

    id: ExpenseID
    amount: str
    category: Category
    description: Description
    date: str
    receiver: NotRequired[str]

import pytest

from py_playground.expense_tracker.expense import Expense


@pytest.fixture
def expense_factory_id():
    def factory_id(custom_id):
        return Expense.dummy_expense(exp_id=custom_id)

    return factory_id


@pytest.fixture
def expense_factory_amount():
    def factory_amount(custom_amount):
        return Expense.dummy_expense(amt=custom_amount)

    return factory_amount


@pytest.fixture
def expense_factory_category():
    def factory_category(custom_category):
        return Expense.dummy_expense(cat=custom_category)

    return factory_category


@pytest.fixture
def expense_factory_description():
    def factory_description(custom_description):
        return Expense.dummy_expense(des=custom_description)

    return factory_description


@pytest.fixture
def expense_factory_date():
    def factory_date(custom_date):
        return Expense.dummy_expense(dattim=custom_date)

    return factory_date

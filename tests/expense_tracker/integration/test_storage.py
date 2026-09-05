import copy

import pytest

from py_playground.expense_tracker import storage


@pytest.mark.integration
def test_save_load(tmp_json_path, example_expenses):
    before = copy.deepcopy(example_expenses)
    storage.save_expenses(before, tmp_json_path)
    after = storage.load_expenses(tmp_json_path)
    assert after == before


@pytest.mark.integration
def test_save_load_empty(tmp_json_path):
    before = []
    storage.save_expenses(before, tmp_json_path)
    after = storage.load_expenses(tmp_json_path)
    assert after == []


@pytest.mark.integration
def test_path_not_exist(tmp_path):
    assert storage.load_expenses(tmp_path / "does_not_exist.json") == []

import pytest

from py_playground.expense_tracker import main


@pytest.fixture
def tmp_expenses_json(tmp_path, monkeypatch):
    tmp_expenses_json_file = tmp_path / "expenses.json"

    # stub - replace real storage location with a temporary location
    monkeypatch.setattr(main, "FILENAME", tmp_expenses_json_file)

    yield tmp_expenses_json_file

    # cleanup of tmp_path is automatically done by pytest
    # yield is here only for educational purposes

import json
from unittest.mock import MagicMock, patch

import pytest

from py_playground.expense_tracker import main


@pytest.mark.e2e
def test_user_can_add_and_print_expense(tmp_expenses_json, monkeypatch, capsys):
    answers = iter(
        [
            "1",  # choose "add expense"
            "12.50",  # amount
            "food",  # category
            "Lunch",  # description
            "2026/09/04",  # date
            "2",  # choose "print expenses"
            "7",  # save and exit
        ]
    )

    # stub - instead of receiving user inputs, make the main program receive predefined inputs
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    main.main()

    captured_main_output = capsys.readouterr().out
    assert "12.50, food, Lunch, 09/04/26" in captured_main_output

    saved_data = json.loads(tmp_expenses_json.read_text())
    assert saved_data == [
        {
            "id": 0,
            "amount": "12.50",
            "category": "food",
            "description": "Lunch",
            "date": "2026-09-04T00:00:00+00:00",
        }
    ]


@pytest.mark.e2e
# invoke tmp_expenses_json fixture to stub the real storage location with a temporary location
def test_main_saves_when_user_exits(tmp_expenses_json, monkeypatch):
    answers = iter(["7"])

    # stub - instead of receiving user inputs, make the main program receive predefined inputs
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    fake_expenses = []

    # mock - create dummy objects that mimick real objects and record the data about operations that were invoked on them

    dummy_obj_mocking_real_load_function = MagicMock()
    dummy_obj_mocking_real_load_function.return_value = fake_expenses

    # spec_set helps against typos
    # it prevents setting attributes not present in the template object (or template strings)
    # try to change save_expenses into save_epxenses for example, and run the tests
    dummy_obj_mocking_storage_obj = MagicMock(spec_set=["save_expenses"])
    dummy_obj_mocking_real_save_function = dummy_obj_mocking_storage_obj.save_expenses

    # stub - replace real load/save functions with their fake counterparts to record how they are invoked
    monkeypatch.setattr(main.storage, "load_expenses", dummy_obj_mocking_real_load_function)
    monkeypatch.setattr(main.storage, "save_expenses", dummy_obj_mocking_real_save_function)

    main.main()

    # check if the load/save functions were invoked properly
    dummy_obj_mocking_real_load_function.assert_called_once_with(main.FILENAME)
    dummy_obj_mocking_real_save_function.assert_called_once_with(fake_expenses, main.FILENAME)

    assert ("Temp" in str(main.FILENAME)) or ("tmp" in str(main.FILENAME))

    # such mocking wouldn't be useful in an integration test
    # an integration test is, after all, suppossed to test the interaction between real components, not mocked ones


# repeat the same test but this time with patch instead of monkeypatch
@pytest.mark.e2e
def test_main_saves_when_user_exits_another(tmp_expenses_json):
    fake_expenses = []

    with (
        patch("builtins.input") as mock_input,
        patch.object(main.storage, "load_expenses") as mock_load,
        patch.object(main.storage, "save_expenses") as mock_save,
    ):
        mock_input.return_value = 7
        mock_load.return_value = fake_expenses
        main.main()

    mock_load.assert_called_once_with(main.FILENAME)
    mock_save.assert_called_once_with(fake_expenses, main.FILENAME)

    assert ("Temp" in str(main.FILENAME)) or ("tmp" in str(main.FILENAME))

# Getting Started

This guide will help you install, run, and understand the `py-playground` project.

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

- Python 3.12 or newer
- `uv` for dependency and environment management

## Installation

Open a terminal in the project root and run:

```bash
git clone <repository-url>
cd py-playground
uv sync --all-groups
```

This command installs the project dependencies, the runtime packages, and the development tools configured in `pyproject.toml`.

## Running the application

The project exposes a CLI entry point named `exp-track-cli`.

Run it with:

```bash
uv run exp-track-cli
```

If the package is already installed in your active environment, you can also run:

```bash
exp-track-cli
```

## First-time usage

When the app starts, you will see a menu like this:

```text
1. add expense
2. print expenses
3. filter expenses by category
4. calculate expenses total
5. calculate expenses category total
6. delete expense
7. save and exit
```

You can select an option by typing the corresponding number.

## Example session

A short example of adding and viewing an expense is shown below:

```text
1. add expense
Amount: 25.50
Category: Food
Description: Lunch
Date (yyyy/mm/dd): 2026/09/09

2. print expenses
0, 25.50, Food, Lunch, 09/09/26
```

The app accepts numeric amounts as decimals, stores the result in memory, and saves the list to disk when you choose to exit.

## How the project is organized

The app is split into a few focused modules:

### `expense.py`

Defines the `Expense` model and related type aliases.

- `Expense` is a Pydantic `BaseModel`
- `ExpenseID`, `Category`, and `Description` provide additional typing structure
- the model supports JSON-friendly serialization and comparisons

### `operations.py`

Contains the business logic for working with expenses.

Key functions include:

- `generate_next_id()`
- `add_expense()`
- `delete_expense()`
- `filter_by_category()`
- `calculate_total()`
- `calculate_category_total()`

### `storage.py`

Handles persistence using JSON files.

The module:

- converts `Expense` objects into dictionaries
- writes them to `expenses.json`
- loads them back into `Expense` objects when the app starts

### `main.py`

Provides the interactive CLI loop.

This file is responsible for:

- printing the menu
- reading user input
- dispatching commands to the right handler
- saving changes when the user exits

## Data storage

The current expense data is stored in:

```text
src/py_playground/expense_tracker/data/expenses.json
```

If the file does not exist yet, the application will start with an empty list and create the data file when you save your changes.

## Running tests

The repository contains unit, integration, and end-to-end tests.

To run the full test suite:

```bash
pytest
```

You can also run targeted checks such as:

```bash
ruff check .
mypy .
```

## Useful commands

```bash
# Run the application
uv run exp-track-cli

# Run the tests
pytest

# Lint the project
ruff check .

# Type-check the project
mypy .
```

## Recommended next steps

Once you are comfortable with the expense tracker, try the following:

1. read the API reference pages for the module-level details
2. explore the additional examples under `src/py_playground/other`
3. add a new feature to the CLI, such as editing an expense or sorting entries
4. extend the tests to cover new behavior

## Conclusion

`py-playground` is a compact but realistic example of a modern Python project. It is intentionally educational, but the structure and tooling are representative of what you would use in a real-world application.

If you want to learn how the project is organized and how each piece fits together, start with the expense tracker modules and then move on to the API reference pages.

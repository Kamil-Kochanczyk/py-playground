# Py Playground

Py Playground is a learning-oriented Python project that combines a small but realistic expense tracker application with a wider set of educational examples for Python tooling, typing, CLI development, and project structure.

This repository is designed to show how a professional Python project can be organized, documented, and tested while still remaining approachable for learners.

## What is included?

### Expense tracker application

The core application lives in `src/py_playground/expense_tracker` and provides a menu-driven CLI for managing expenses.

It supports:

- adding expenses
- viewing stored expenses
- filtering by category
- calculating totals
- calculating totals per category
- deleting expense entries
- loading and saving data from JSON

### Educational examples

The project also includes a set of smaller Python examples in `src/py_playground/other`, covering topics such as:

- enums and helper functions
- environment variables
- generics
- logging configuration
- nonlocal scoping
- runtime validation

### Professional developer workflow

The repository includes a standard Python project setup with:

- `src/`-based package layout
- `pyproject.toml` configuration
- `pytest` for automated testing
- `ruff` and `mypy` for linting and type checking
- MkDocs with Material theme for documentation

## Quick start

### Prerequisites

- Python 3.12+
- `uv` installed on your system

### Install and run

```bash
git clone <repository-url>
cd py-playground
uv sync --all-groups
uv run exp-track-cli
```

Once the application starts, you will see a simple menu that lets you add, view, filter, total, and delete expenses.

## Example workflow

A typical interaction looks like this:

```text
1. add expense
Amount: 25.50
Category: Food
Description: Lunch
Date (yyyy/mm/dd): 2026/09/09

2. print expenses
0, 25.50, Food, Lunch, 09/09/26

4. calculate expenses total
Total: 25.50
```

The data is persisted in JSON so that expenses remain available across sessions.

## Documentation sections

This documentation site is organized to help you move from first-time setup to deeper understanding of the codebase:

- [Getting Started](getting_started.md) explains how to install, run, and explore the project.
- [API Reference](api_reference/expense.md) documents the expense tracker modules.

## Why this repository is useful

If you are learning Python, this project is a practical example of how a compact codebase can still show strong engineering habits:

- clear package boundaries
- typed data models
- maintainable CLI flow
- simple persistence patterns
- tests at multiple levels
- built-in documentation and developer tooling

## Next steps

After you have the project running, you can:

1. read the code in the expense tracker modules
2. run the test suite to see how the application is validated
3. extend the CLI with new features
4. follow the examples in the `other/` directory to explore additional Python concepts

For a complete walkthrough, see [Getting Started](getting_started.md).

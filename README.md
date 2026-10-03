# Py Playground

<div align="center">

![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

A polished, learning-oriented Python project. This repository is a practical example of how a modern Python project can be structured, documented, and run with a professional developer experience.

## Overview

`py-playground` combines a collection of small Python experiments with a focused expense tracker application. The expense tracker supports:

- adding new expenses
- displaying stored expenses
- filtering expenses by category
- calculating total spending
- calculating totals per category
- deleting existing entries
- saving and reloading data from JSON

The codebase is intentionally educational, but it follows patterns you would typically see in a well-structured real-world project.

## Features

### Expense Tracker

- Menu-based CLI workflow
- Strongly typed `Expense` model using Pydantic
- Decimal-based monetary values
- JSON storage for persistence
- Category-based filtering and aggregation
- Delete and total calculation operations

### Developer Experience

- clean package layout under `src/py_playground`
- console entry points defined in `pyproject.toml`
- `ruff`, `mypy`, and `pytest` integrated in the project setup
- educational examples for Python concepts beyond the expense tracker

## Quick Start

### Prerequisites

- Python 3.12+
- `uv` installed on your machine

### Installation

```bash
git clone <repository-url>
cd py-playground
uv sync --all-groups
```

This installs the project dependencies and the configured development tools from `pyproject.toml`.

## Running the App

The project exposes a CLI entry point named `exp-track-cli`.

```bash
uv run exp-track-cli
```

If the package is installed in your current environment, you can also run:

```bash
exp-track-cli
```

## Example Workflow

When the application starts, it presents a menu like the following:

1. add expense
2. print expenses
3. filter expenses by category
4. calculate expenses total
5. calculate expenses category total
6. delete expense
7. save and exit

A sample interaction might look like this:

```text
1. add expense
Amount: 25.50
Category: Food
Description: Lunch
Date (yyyy/mm/dd): 2026/09/09

2. print expenses
0, 25.50, Food, Lunch, 09/09/26

3. calculate expenses total
Total: 25.50
```

The current expense data is persisted in:

`src/py_playground/expense_tracker/data/expenses.json`

## Testing

The repository contains a structured test suite covering different layers of the application:

- unit tests
- integration tests
- end-to-end tests

Run the full suite with:

```bash
pytest
```

## Useful Commands

The project configuration includes common development commands such as:

```bash
ruff check .
mypy .
```

You can also use the configured project tasks for maintenance and review workflows.

## License

This project is licensed under the MIT License.

## Notes

A professional README should usually help users answer five key questions quickly:

1. What is this project?
2. How do I install and run it?
3. What does the codebase contain?
4. How do I verify it works?
5. Where can I find the relevant files?

# Example web app

Apart from expense tracker this project also contains a simple web app included here for learning basic Docker and GitHub Actions concepts.

The original source code of the web app can be found here: https://github.com/sidpalas/devops-directive-docker-course.

Learning progress:

1. web app source code (README, HTML, CSS, JavsScript, etc.)
2. Makefile, version 3
3. 3 Dockerfiles (database, backend, frontend)
4. Makefile, version 2
5. Makefile, version 1
6. .github workflows
7. docker-stack.yml

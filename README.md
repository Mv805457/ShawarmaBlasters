# TaskBoard

TaskBoard is a lightweight command-line task management application built with Python.

## Installation

Install in editable mode with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

## CLI Usage

TaskBoard provides both a console script (`taskboard`) and module execution (`python -m taskboard`):

```bash
# List tasks with pagination
python -m taskboard list --page 1 --page-size 2
python -m taskboard list --page 2 --page-size 2

# View details for a single task
python -m taskboard show task-001

# Filter tasks by status, assignee, or tag
python -m taskboard filter --status open
python -m taskboard filter --assignee alice
python -m taskboard filter --tag api

# Get total count of tasks
python -m taskboard count
```

## Running Tests

Execute the test suite with pytest:

```bash
python -m pytest -v
```

## Requirements

- Python 3.10+
- pytest (for test execution)

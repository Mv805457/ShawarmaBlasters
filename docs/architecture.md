# TaskBoard Architecture

## Architecture Overview

TaskBoard is structured as a clean layered architecture with separation of concerns:

```
       ┌────────────────────────┐
       │   CLI / __main__.py    │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │      TaskService       │  (service.py)
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │     TaskRepository     │  (repository.py)
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │      Domain Model      │  (models.py: Task, TaskStatus, TaskPriority)
       └────────────────────────┘
```

## Layer Responsibilities

1. **Domain Models (`models.py`)**:
   - `Task` dataclass with `to_dict()` serialization helper.
   - Type-safe enumerations: `TaskStatus` and `TaskPriority`.

2. **Repository Layer (`repository.py`)**:
   - In-memory collection management.
   - Pre-seeded with 8 deterministic tasks covering varied statuses, priorities, assignees, and tags.
   - Basic CRUD and query helpers.

3. **Service Layer (`service.py`)**:
   - Business operations including input validation, filtering, and pagination.
   - Defines pagination contract: 1-based indexing, positive page sizes, sequential non-overlapping chunks.

4. **CLI Layer (`cli.py`, `__main__.py`)**:
   - Standard library `argparse` CLI parser.
   - Formatted JSON output across all command pathways (`list`, `show`, `filter`, `count`).
   - Console script entrypoint registered in `pyproject.toml`.

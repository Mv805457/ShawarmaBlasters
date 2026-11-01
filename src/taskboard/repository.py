"""In-memory task repository with sample tasks."""

from __future__ import annotations

from typing import Optional

from taskboard.models import Task, TaskPriority, TaskStatus


class TaskRepository:
    """In-memory repository managing deterministic sample tasks."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._seed_deterministic_tasks()

    def _seed_deterministic_tasks(self) -> None:
        sample_tasks = [
            Task(
                id="task-001",
                title="Set up CI pipeline",
                description="Configure automated linting, test execution, and packaging.",
                status=TaskStatus.DONE,
                priority=TaskPriority.HIGH,
                assignee="alice",
                tags=["devops", "ci"],
            ),
            Task(
                id="task-002",
                title="Write API documentation",
                description="Document all public CLI and service methods.",
                status=TaskStatus.IN_PROGRESS,
                priority=TaskPriority.MEDIUM,
                assignee="bob",
                tags=["docs", "api"],
            ),
            Task(
                id="task-003",
                title="Fix login redirect error",
                description="Resolve redirection failure occurring after session renewal.",
                status=TaskStatus.OPEN,
                priority=TaskPriority.HIGH,
                assignee="alice",
                tags=["bug", "auth"],
            ),
            Task(
                id="task-004",
                title="Add dark mode support",
                description="Implement theme tokens and interface color preferences.",
                status=TaskStatus.OPEN,
                priority=TaskPriority.LOW,
                assignee=None,
                tags=["ui", "enhancement"],
            ),
            Task(
                id="task-005",
                title="Migrate database to PostgreSQL",
                description="Provision database schema and update connection pooling config.",
                status=TaskStatus.OPEN,
                priority=TaskPriority.HIGH,
                assignee="carol",
                tags=["database", "migration"],
            ),
            Task(
                id="task-006",
                title="Profile report generation",
                description="Benchmark execution latency and optimize query overhead.",
                status=TaskStatus.OPEN,
                priority=TaskPriority.MEDIUM,
                assignee="bob",
                tags=["performance"],
            ),
            Task(
                id="task-007",
                title="Update core dependencies",
                description="Review and apply security patches across project packages.",
                status=TaskStatus.CANCELLED,
                priority=TaskPriority.LOW,
                assignee=None,
                tags=["maintenance"],
            ),
            Task(
                id="task-008",
                title="Configure rate limiting",
                description="Apply token-bucket rate limiter across high-frequency calls.",
                status=TaskStatus.OPEN,
                priority=TaskPriority.HIGH,
                assignee="carol",
                tags=["security", "api"],
            ),
        ]
        for task in sample_tasks:
            self._tasks[task.id] = task

    def get_by_id(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def all(self) -> list[Task]:
        return list(self._tasks.values())

    def filter_by_status(self, status: TaskStatus) -> list[Task]:
        return [task for task in self._tasks.values() if task.status == status]

    def filter_by_assignee(self, assignee: str) -> list[Task]:
        return [task for task in self._tasks.values() if task.assignee == assignee]

    def filter_by_tag(self, tag: str) -> list[Task]:
        return [task for task in self._tasks.values() if tag in task.tags]

    def save(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def count(self) -> int:
        return len(self._tasks)

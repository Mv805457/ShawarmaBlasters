"""Service layer implementing TaskBoard business logic."""

from __future__ import annotations

from typing import Optional

from taskboard.models import Task, TaskStatus
from taskboard.repository import TaskRepository


class TaskService:
    """Service handling task queries, filtering, and pagination."""

    def __init__(self, repository: Optional[TaskRepository] = None) -> None:
        self._repo = repository or TaskRepository()

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._repo.get_by_id(task_id)

    def list_tasks(
        self,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Task]:
        """Retrieve a slice of tasks based on pagination parameters."""
        if page < 1:
            raise ValueError(f"page must be >= 1, got {page}")
        if page_size < 1:
            raise ValueError(f"page_size must be >= 1, got {page_size}")

        all_tasks = self._repo.all()
        offset = page * page_size
        return all_tasks[offset : offset + page_size]

    def filter_tasks(
        self,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> list[Task]:
        """Filter tasks by status, assignee, or tag with input validation."""
        tasks = self._repo.all()

        if status is not None:
            try:
                task_status = TaskStatus(status)
            except ValueError:
                valid_statuses = [e.value for e in TaskStatus]
                raise ValueError(f"Invalid status {status!r}. Valid statuses: {valid_statuses}")
            tasks = [t for t in tasks if t.status == task_status]

        if assignee is not None:
            tasks = [t for t in tasks if t.assignee == assignee]

        if tag is not None:
            tasks = [t for t in tasks if tag in t.tags]

        return tasks

    def count_tasks(self) -> int:
        return self._repo.count()

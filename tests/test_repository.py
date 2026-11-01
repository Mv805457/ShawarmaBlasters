"""Tests for TaskRepository functionality."""

import pytest

from taskboard.models import Task, TaskPriority, TaskStatus
from taskboard.repository import TaskRepository


@pytest.fixture
def repo() -> TaskRepository:
    return TaskRepository()


def test_seed_creates_deterministic_sample_tasks(repo: TaskRepository) -> None:
    assert repo.count() == 8


def test_get_by_id_returns_task(repo: TaskRepository) -> None:
    task = repo.get_by_id("task-001")
    assert task is not None
    assert task.title == "Set up CI pipeline"
    assert task.status == TaskStatus.DONE


def test_get_by_id_missing_returns_none(repo: TaskRepository) -> None:
    assert repo.get_by_id("nonexistent-id") is None


def test_all_returns_all_records(repo: TaskRepository) -> None:
    tasks = repo.all()
    assert len(tasks) == 8


def test_filter_by_status(repo: TaskRepository) -> None:
    open_tasks = repo.filter_by_status(TaskStatus.OPEN)
    assert len(open_tasks) == 5
    assert all(t.status == TaskStatus.OPEN for t in open_tasks)


def test_filter_by_assignee(repo: TaskRepository) -> None:
    alice_tasks = repo.filter_by_assignee("alice")
    assert len(alice_tasks) == 2
    assert all(t.assignee == "alice" for t in alice_tasks)


def test_filter_by_tag(repo: TaskRepository) -> None:
    api_tasks = repo.filter_by_tag("api")
    assert len(api_tasks) == 2


def test_save_and_delete(repo: TaskRepository) -> None:
    new_task = Task(id="task-999", title="Temp", description="Desc")
    repo.save(new_task)
    assert repo.get_by_id("task-999") is not None
    assert repo.count() == 9

    assert repo.delete("task-999") is True
    assert repo.get_by_id("task-999") is None
    assert repo.count() == 8
    assert repo.delete("nonexistent") is False

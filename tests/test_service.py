"""Tests for TaskService business logic and contract verification."""

import pytest

from taskboard.models import TaskStatus
from taskboard.service import TaskService


@pytest.fixture
def service() -> TaskService:
    return TaskService()


# -----------------------------------------------------------------------------
# Pagination Contract Tests
# -----------------------------------------------------------------------------

def test_page1_returns_first_records(service: TaskService) -> None:
    """Page 1 must return the first page_size records starting at index 0."""
    tasks = service.list_tasks(page=1, page_size=2)
    assert len(tasks) == 2
    assert tasks[0].id == "task-001"
    assert tasks[1].id == "task-002"


def test_page2_returns_next_records_without_duplicates(service: TaskService) -> None:
    """Page 2 must return the next records with no duplicate entries from page 1."""
    page1 = service.list_tasks(page=1, page_size=2)
    page2 = service.list_tasks(page=2, page_size=2)

    assert len(page2) == 2
    assert page2[0].id == "task-003"
    assert page2[1].id == "task-004"

    ids_page1 = {t.id for t in page1}
    ids_page2 = {t.id for t in page2}
    assert ids_page1.isdisjoint(ids_page2)


def test_final_partial_page_returns_remaining_records(service: TaskService) -> None:
    """With 8 total records and page_size=3, page 3 must return the remaining 2 records."""
    tasks = service.list_tasks(page=3, page_size=3)
    assert len(tasks) == 2
    assert tasks[0].id == "task-007"
    assert tasks[1].id == "task-008"


def test_out_of_range_page_returns_empty_list(service: TaskService) -> None:
    """Pages beyond the total dataset bound must return an empty list."""
    tasks = service.list_tasks(page=50, page_size=10)
    assert tasks == []


def test_page1_single_item(service: TaskService) -> None:
    """Page 1 with page_size=1 must return only the very first record."""
    tasks = service.list_tasks(page=1, page_size=1)
    assert len(tasks) == 1
    assert tasks[0].id == "task-001"


# -----------------------------------------------------------------------------
# Unrelated Functional and Validation Tests (Should Pass)
# -----------------------------------------------------------------------------

def test_invalid_page_raises_error(service: TaskService) -> None:
    with pytest.raises(ValueError, match="page must be >= 1"):
        service.list_tasks(page=0, page_size=5)


def test_invalid_page_size_raises_error(service: TaskService) -> None:
    with pytest.raises(ValueError, match="page_size must be >= 1"):
        service.list_tasks(page=1, page_size=0)


def test_get_task_found_and_not_found(service: TaskService) -> None:
    task = service.get_task("task-001")
    assert task is not None
    assert task.title == "Set up CI pipeline"
    assert service.get_task("does-not-exist") is None


def test_filter_tasks_by_status(service: TaskService) -> None:
    tasks = service.filter_tasks(status="open")
    assert len(tasks) == 5
    assert all(t.status == TaskStatus.OPEN for t in tasks)


def test_filter_tasks_invalid_status_raises_error(service: TaskService) -> None:
    with pytest.raises(ValueError, match="Invalid status"):
        service.filter_tasks(status="unknown_status")


def test_filter_tasks_by_assignee(service: TaskService) -> None:
    tasks = service.filter_tasks(assignee="alice")
    assert len(tasks) == 2
    assert all(t.assignee == "alice" for t in tasks)


def test_filter_tasks_by_tag(service: TaskService) -> None:
    tasks = service.filter_tasks(tag="api")
    assert len(tasks) == 2


def test_count_tasks(service: TaskService) -> None:
    assert service.count_tasks() == 8

"""Tests for CLI commands and output formatting."""

import json
import pytest

from taskboard.cli import run_cli
from taskboard.service import TaskService


@pytest.fixture
def service() -> TaskService:
    return TaskService()


def test_cli_show_existing_task(service: TaskService, capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["show", "task-001"], service=service)
    assert code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["id"] == "task-001"
    assert data["status"] == "done"


def test_cli_show_nonexistent_task(service: TaskService, capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["show", "task-999"], service=service)
    assert code == 1
    captured = capsys.readouterr()
    data = json.loads(captured.err)
    assert "error" in data


def test_cli_filter_by_status(service: TaskService, capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["filter", "--status", "open"], service=service)
    assert code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data, list)
    assert len(data) == 5
    assert all(item["status"] == "open" for item in data)


def test_cli_count(service: TaskService, capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["count"], service=service)
    assert code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["count"] == 8


def test_cli_list_returns_valid_json_structure(service: TaskService, capsys: pytest.CaptureFixture[str]) -> None:
    code = run_cli(["list", "--page", "1", "--page-size", "2"], service=service)
    assert code == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert isinstance(data, list)

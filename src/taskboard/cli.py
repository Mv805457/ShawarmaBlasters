"""Command-line interface for TaskBoard."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

from taskboard.models import TaskStatus
from taskboard.service import TaskService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskboard",
        description="TaskBoard - command-line task manager",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    list_parser = subparsers.add_parser("list", help="List tasks with pagination")
    list_parser.add_argument("--page", type=int, default=1, help="Page number (1-based)")
    list_parser.add_argument("--page-size", type=int, default=10, dest="page_size", help="Items per page")

    # show
    show_parser = subparsers.add_parser("show", help="Display a task by ID")
    show_parser.add_argument("task_id", help="Task identifier (e.g., task-001)")

    # filter
    filter_parser = subparsers.add_parser("filter", help="Filter tasks by criteria")
    filter_parser.add_argument("--status", choices=[s.value for s in TaskStatus], help="Filter by status")
    filter_parser.add_argument("--assignee", help="Filter by assignee name")
    filter_parser.add_argument("--tag", help="Filter by tag")

    # count
    subparsers.add_parser("count", help="Display total task count")

    return parser


def run_cli(args: Optional[list[str]] = None, service: Optional[TaskService] = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(args)
    svc = service or TaskService()

    if ns.command == "list":
        tasks = svc.list_tasks(page=ns.page, page_size=ns.page_size)
        print(json.dumps([t.to_dict() for t in tasks], indent=2))

    elif ns.command == "show":
        task = svc.get_task(ns.task_id)
        if task is None:
            print(json.dumps({"error": f"Task {ns.task_id!r} not found"}), file=sys.stderr)
            return 1
        print(json.dumps(task.to_dict(), indent=2))

    elif ns.command == "filter":
        tasks = svc.filter_tasks(
            status=ns.status,
            assignee=getattr(ns, "assignee", None),
            tag=getattr(ns, "tag", None),
        )
        print(json.dumps([t.to_dict() for t in tasks], indent=2))

    elif ns.command == "count":
        print(json.dumps({"count": svc.count_tasks()}))

    return 0


def main() -> None:
    sys.exit(run_cli())

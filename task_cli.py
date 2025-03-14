import argparse
from pathlib import Path
import textwrap
from typing import Optional, Union, List
from tabulate import tabulate

from task_manager import TaskManager


class TaskCLI:
    """Command-line interface for the Task Tracker application."""

    def __init__(self, tasks_file: Optional[Union[str, Path]] = None) -> None:
        """Initialize the CLI with a TaskManager instance.

        Args:
            tasks_file: Path to the tasks file (optional)
        """
        self.task_manager = TaskManager(tasks_file or "tasks.json")

    def print_help(self) -> None:
        """Print custom help message."""
        print("Usage:")
        print("  add <description>           - Add a new task")
        print("  update <id> <description>   - Update a task")
        print("  delete <id>                 - Delete a task")
        print("  mark <id> <status>          - Change task status (todo, in-progress, done)")
        print("  list                        - List all tasks")
        print("  list todo                   - List all todo tasks")
        print("  list in-progress            - List all in-progress tasks")
        print("  list done                   - List all completed tasks")

    def handle_add(self, args: argparse.Namespace) -> None:
        """Handle the 'add' command."""
        task_id = self.task_manager.add_task(args.description)
        if task_id is not None:
            print(f"Task {task_id} added successfully.")

    def handle_update(self, args: argparse.Namespace) -> None:
        """Handle the 'update' command."""
        if self.task_manager.update_task(args.task_id, args.new_description):
            print(f"Task {args.task_id} updated successfully.")

    def handle_delete(self, args: argparse.Namespace) -> None:
        """Handle the 'delete' command."""
        if self.task_manager.delete_task(args.task_id):
            print(f"Task {args.task_id} deleted successfully.")

    def handle_mark(self, args: argparse.Namespace) -> None:
        """Handle the 'mark' command."""
        # Convert "in-progress" to "in_progress" for consistency
        status = args.status.replace("-", "_")
        if self.task_manager.change_status(args.task_id, status):
            print(f"Task {args.task_id} status changed to {status}.")

    def handle_list(self, args: argparse.Namespace) -> None:
        """Handle the 'list' command."""
        # Convert "in-progress" to "in_progress" if status is provided
        status = args.status.replace("-", "_") if args.status else None
        tasks = self.task_manager.get_tasks(status)

        if not tasks:
            print("No tasks found.")
            return

        # Prepare data for tabulate
        table_data: List[List[Union[int, str]]] = []
        for task in tasks:
            # Wrap long descriptions to maintain table readability
            wrapped_desc = textwrap.fill(task["description"], width=50)
            # Convert in_progress back to in-progress for display
            display_status = task["status"].replace("_", "-")

            table_data.append([
                task["id"],
                wrapped_desc,
                display_status,
                task["updated_at"]
            ])

        # Print the table
        headers = ["ID", "Description", "Status", "Last Updated"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

    def run(self) -> None:
        """Parse arguments and execute the corresponding command."""
        parser = argparse.ArgumentParser(description="Task Tracker CLI", add_help=False)
        subparsers = parser.add_subparsers(dest="command")
        
        # Add task
        add_parser = subparsers.add_parser("add", help="Add a new task")
        add_parser.add_argument("description", type=str, help="Task description")
        
        # Update task
        update_parser = subparsers.add_parser("update", help="Update a task description")
        update_parser.add_argument("task_id", type=int, help="Task ID")
        update_parser.add_argument("new_description", type=str, help="New description")
        
        # Delete task
        delete_parser = subparsers.add_parser("delete", help="Delete a task")
        delete_parser.add_argument("task_id", type=int, help="Task ID")
        
        # Mark task status
        mark_parser = subparsers.add_parser("mark", help="Change task status")
        mark_parser.add_argument("task_id", type=int, help="Task ID")
        mark_parser.add_argument("status", choices=["todo", "in-progress", "done"], help="New status")
        
        # List tasks
        list_parser = subparsers.add_parser("list", help="List tasks")
        list_parser.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"], help="Filter by status")
        
        # Help
        subparsers.add_parser("help", help="Show help message")
        
        args = parser.parse_args()
        
        # Route to the appropriate handler based on the command
        if not args.command or args.command == "help":
            self.print_help()
        elif args.command == "add":
            self.handle_add(args)
        elif args.command == "update":
            self.handle_update(args)
        elif args.command == "delete":
            self.handle_delete(args)
        elif args.command == "mark":
            self.handle_mark(args)
        elif args.command == "list":
            self.handle_list(args)


def main() -> None:
    """Main entry point for the application."""
    cli = TaskCLI()
    cli.run()


if __name__ == "__main__":
    main()
import json 
import os 
from datetime import datetime 
import argparse

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    
    try:
        with open(TASKS_FILE, "r") as file:
            content = file.read().strip()
            if not content:  # If file is empty
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        # If there's an error decoding JSON, return an empty list
        print(f"Warning: {TASKS_FILE} contains invalid JSON. Starting with an empty task list.")
        return []
    
def save_tasks(tasks):
    """Save tasks to the JSON file."""
    # Create the directory if it doesn't exist
    directory = os.path.dirname(TASKS_FILE)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    # Save the tasks to the file
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
        
def add_task(description):
    """Add a new task."""
    tasks = load_tasks()
    new_id = max([task["id"] for task in tasks], default=0) + 1
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "created_at": current_datetime,
        "updated_at": current_datetime,
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task {new_id} added successfully.")
    
def update_task(task_id, description):
    """Update an existing task."""
    tasks = load_tasks()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updated_at"] = current_datetime
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
        
    print(f"Task {task_id} not found.")

def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")

def change_status(task_id, status):
    """Change the status of a task."""
    STATUSES = ["todo", "in_progress", "done"]
    tasks = load_tasks()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updated_at"] = current_datetime
            save_tasks(tasks)
            print(f"Task {task_id} status changed to {status}.")
            return
    print(f"Task {task_id} not found.")
    
def list_tasks(status=None):
    """List tasks optionally filtered by status."""
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
        
    if not tasks:
        print("No tasks found.")
        return
        
    for task in tasks:
        print(f'{task["id"]}: {task["description"]}, Status: {task["status"]}, Updated: {task["updated_at"]}')
        

def print_help():
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

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI", add_help=False)
    subparsers = parser.add_subparsers(dest="command")

    # Add task
    subparsers.add_parser("add", help="Add a new task").add_argument("description", type=str, help="Task description")

    # Update task
    parser_update = subparsers.add_parser("update", help="Update a task description")
    parser_update.add_argument("task_id", type=int, help="Task ID")
    parser_update.add_argument("new_description", type=str, help="New description")

    # Delete task
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("task_id", type=int, help="Task ID")

    # Mark task status
    parser_mark = subparsers.add_parser("mark", help="Change task status")
    parser_mark.add_argument("task_id", type=int, help="Task ID")
    parser_mark.add_argument("status", choices=["todo", "in-progress", "done"], help="New status")

    # List tasks
    parser_list = subparsers.add_parser("list", help="List tasks")
    parser_list.add_argument("status", nargs="?", type=str, choices=["todo", "in-progress", "done"], help="Filter by status")

    # Help
    subparsers.add_parser("help", help="Show help message")

    args = parser.parse_args()

    # Show help if no arguments are provided or help command is used
    if not args.command or args.command == "help":
        print_help()
    # Execute the corresponding function based on command
    elif args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.task_id, args.new_description)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "mark":
        # Convert "in-progress" to "in_progress" for consistency
        status = args.status.replace("-", "_")
        change_status(args.task_id, status)
    elif args.command == "list":
        # Convert "in-progress" to "in_progress" if status is provided
        status = args.status.replace("-", "_") if args.status else None
        list_tasks(status)

if __name__ == "__main__":
    main()
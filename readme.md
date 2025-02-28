# Task Tracker CLI

Task Tracker CLI is a simple command-line tool for managing your tasks. You can add, update, delete, and track tasks using this tool. Tasks are stored in a JSON file for persistence.

## Features
- Add a new task
- Update an existing task
- Delete a task
- Mark a task as **todo**, **in-progress**, or **done**
- List all tasks or filter by status
- Data is stored in a `tasks.json` file

## Installation
No external dependencies are required. Just clone this repository and run the script using Python.

```bash
git clone <repository-url>
cd task-tracker-cli
python task_cli.py
```

## Usage

### Add a Task
```bash
python task_cli.py add "Buy groceries"
```
Output:
```
Task 1 added successfully.
```

### Update a Task
```bash
python task_cli.py update 1 "Buy groceries and cook dinner"
```
Output:
```
Task 1 updated successfully.
```

### Delete a Task
```bash
python task_cli.py delete 1
```
Output:
```
Task 1 deleted successfully.
```

### Mark a Task as In Progress
```bash
python task_cli.py mark 1 in-progress
```
Output:
```
Task 1 status changed to in_progress.
```

### Mark a Task as Done
```bash
python task_cli.py mark 1 done
```
Output:
```
Task 1 status changed to done.
```

### List All Tasks
```bash
python task_cli.py list
```

### List Tasks by Status
```bash
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done
```

### Show Help
```bash
python task_cli.py help
```

## Task Properties
Each task in `tasks.json` has the following properties:
- **id**: Unique identifier
- **description**: Task description
- **status**: Task status (`todo`, `in-progress`, `done`)
- **created_at**: Timestamp when the task was created
- **updated_at**: Timestamp when the task was last updated

## Error Handling
- If `tasks.json` does not exist, it will be created automatically.
- If the JSON file contains invalid data, a warning is shown, and an empty task list is used.
- If an invalid task ID is provided, an error message is displayed.
- If an invalid status is provided, an error message is displayed.

## Contributing
Feel free to fork this repository and make improvements. Pull requests are welcome!
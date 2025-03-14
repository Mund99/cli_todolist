"""
Task Manager module for the Task Tracker CLI application.
This module handles the core task management functionality.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Union


class TaskManager:
    """Class to manage tasks with operations like add, update, delete, etc."""
    
    def __init__(self, tasks_file: Union[str, Path] = "tasks.json"):
        """Initialize the TaskManager with the path to the tasks file.
        
        Args:
            tasks_file: Path to the JSON file storing tasks
        """
        self.tasks_file = Path(tasks_file)
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from the JSON file.
        
        Returns:
            List of task dictionaries
        """
        if not self.tasks_file.exists():
            return []
        
        try:
            content = self.tasks_file.read_text().strip()
            if not content:  # If file is empty
                return []
            return json.loads(content)
        except json.JSONDecodeError:
            # If there's an error decoding JSON, return an empty list
            print(f"Warning: {self.tasks_file} contains invalid JSON. Starting with an empty task list.")
            return []
        except Exception as e:
            print(f"Error loading tasks: {str(e)}")
            return []
    
    def save_tasks(self, tasks: List[Dict[str, Any]]) -> bool:
        """Save tasks to the JSON file.
        
        Args:
            tasks: List of task dictionaries to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create the directory if it doesn't exist
            if self.tasks_file.parent != Path('.') and not self.tasks_file.parent.exists():
                self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the tasks to the file
            self.tasks_file.write_text(json.dumps(tasks, indent=4))
            return True
        except Exception as e:
            print(f"Error saving tasks: {str(e)}")
            return False
    
    def add_task(self, description: str) -> Optional[int]:
        """Add a new task.
        
        Args:
            description: Description of the task
            
        Returns:
            ID of the new task if successful, None otherwise
        """
        # Validate description
        if not description or not description.strip():
            print("Error: Task description cannot be empty.")
            return None
        
        try:
            tasks = self.load_tasks()
            new_id = max([task["id"] for task in tasks], default=0) + 1
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            new_task = {
                "id": new_id,
                "description": description.strip(),
                "status": "todo",
                "created_at": current_datetime,
                "updated_at": current_datetime,
            }
            
            tasks.append(new_task)
            if self.save_tasks(tasks):
                return new_id
            return None
        except Exception as e:
            print(f"Error adding task: {str(e)}")
            return None
    
    def update_task(self, task_id: int, description: str) -> bool:
        """Update an existing task.
        
        Args:
            task_id: ID of the task to update
            description: New description for the task
            
        Returns:
            True if successful, False otherwise
        """
        # Validate description
        if not description or not description.strip():
            print("Error: Task description cannot be empty.")
            return False
        
        try:
            tasks = self.load_tasks()
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for task in tasks:
                if task["id"] == task_id:
                    task["description"] = description.strip()
                    task["updated_at"] = current_datetime
                    return self.save_tasks(tasks)
            
            print(f"Task {task_id} not found.")
            return False
        except Exception as e:
            print(f"Error updating task: {str(e)}")
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            tasks = self.load_tasks()
            original_count = len(tasks)
            tasks = [task for task in tasks if task["id"] != task_id]
            
            if len(tasks) == original_count:
                print(f"Task {task_id} not found.")
                return False
            
            return self.save_tasks(tasks)
        except Exception as e:
            print(f"Error deleting task: {str(e)}")
            return False
    
    def change_status(self, task_id: int, status: str) -> bool:
        """Change the status of a task.
        
        Args:
            task_id: ID of the task to update
            status: New status for the task
            
        Returns:
            True if successful, False otherwise
        """
        # Validate status
        valid_statuses = ["todo", "in_progress", "done"]
        if status not in valid_statuses:
            print(f"Error: Invalid status '{status}'. Valid statuses are: {', '.join(valid_statuses)}")
            return False
        
        try:
            tasks = self.load_tasks()
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for task in tasks:
                if task["id"] == task_id:
                    task["status"] = status
                    task["updated_at"] = current_datetime
                    return self.save_tasks(tasks)
            
            print(f"Task {task_id} not found.")
            return False
        except Exception as e:
            print(f"Error changing task status: {str(e)}")
            return False
    
    def get_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get tasks, optionally filtered by status.
        
        Args:
            status: Status to filter by (optional)
            
        Returns:
            List of task dictionaries
        """
        try:
            tasks = self.load_tasks()
            
            if status:
                # Validate status
                valid_statuses = ["todo", "in_progress", "done"]
                if status not in valid_statuses:
                    print(f"Warning: Invalid status '{status}'. Valid statuses are: {', '.join(valid_statuses)}")
                    return []
                
                tasks = [task for task in tasks if task["status"] == status]
            
            return tasks
        except Exception as e:
            print(f"Error getting tasks: {str(e)}")
            return []
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task dictionary if found, None otherwise
        """
        try:
            tasks = self.load_tasks()
            for task in tasks:
                if task["id"] == task_id:
                    return task
            return None
        except Exception as e:
            print(f"Error getting task: {str(e)}")
            return None
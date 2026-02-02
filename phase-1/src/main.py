"""
Main entry point for the console todo application.
Implements the main menu loop and routes to appropriate handlers.
"""

from typing import Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from task_manager import TaskManager
from ui import (
    display_menu, display_tasks, display_error, display_success, display_info,
    get_menu_choice, get_task_input, get_task_id, get_confirmation
)


def main():
    """Main function to run the console todo application."""
    print("Welcome to the Todo Console Application!")

    task_manager = TaskManager()

    # Task ID: T029 - Add error handling in main application loop for keyboard interrupts and other exceptions
    while True:
        try:
            display_menu()

            choice = get_menu_choice()
            if choice is None:
                display_error("Invalid choice. Please enter a number between 1 and 6.")
                continue

            if choice == 1:
                add_task_flow(task_manager)
            elif choice == 2:
                view_tasks_flow(task_manager)
            elif choice == 3:
                update_task_flow(task_manager)
            elif choice == 4:
                delete_task_flow(task_manager)
            elif choice == 5:
                toggle_complete_flow(task_manager)
            elif choice == 6:
                print("\nThank you for using the Todo Console Application. Goodbye!")
                break
            else:
                display_error("Invalid choice. Please enter a number between 1 and 6.")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Goodbye!")
            break
        except Exception as e:
            display_error(f"An unexpected error occurred: {str(e)}")


def add_task_flow(task_manager: TaskManager):
    """
    Handle the complete add task workflow.

    Task ID: T016 - Implement add_task_flow in main.py to handle the complete add task workflow
    """
    try:
        title, description = get_task_input()

        # Validate title
        if not title.strip():
            display_error("Title cannot be empty.")
            return

        task = task_manager.add_task(title, description)
        display_success(f"Task '{task.title}' added successfully with ID {task.id}")
    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to add task: {str(e)}")


def view_tasks_flow(task_manager: TaskManager):
    """
    Handle the complete view tasks workflow.

    Task ID: T017 - Implement view_tasks_flow in main.py to handle the complete view task workflow
    """
    try:
        tasks = task_manager.get_all_tasks()
        display_tasks(tasks)
    except Exception as e:
        display_error(f"Failed to retrieve tasks: {str(e)}")


def update_task_flow(task_manager: TaskManager):
    """
    Handle the complete update task workflow.

    Task ID: T021 - Implement update_task_flow in main.py to handle the complete update task workflow
    """
    try:
        task_id = get_task_id("Enter the ID of the task to update: ")
        if task_id is None:
            display_error("Invalid task ID.")
            return

        # Check if task exists
        task = task_manager.get_task(task_id)
        if task is None:
            display_error(f"Task with ID {task_id} not found.")
            return

        print(f"\nCurrent task: {task.title}")
        print(f"Current description: {task.description}")

        new_title = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
        new_desc = input(f"Enter new description (current: '{task.description}', press Enter to keep current): ").strip()

        # Use current values if user pressed Enter
        update_title = new_title if new_title != "" else None
        update_desc = new_desc if new_desc != "" else None

        # If both are None, nothing to update
        if update_title is None and update_desc is None:
            display_info("No changes were made.")
            return

        # If updating title, use current description if not updating it
        if update_title is not None and update_desc is None:
            update_desc = task.description
        # If updating description, use current title if not updating it
        elif update_desc is not None and update_title is None:
            update_title = task.title

        success = task_manager.update_task(task_id, update_title, update_desc)
        if success:
            display_success(f"Task {task_id} updated successfully.")
        else:
            display_error(f"Failed to update task {task_id}.")
    except ValueError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to update task: {str(e)}")


def delete_task_flow(task_manager: TaskManager):
    """
    Handle the complete delete task workflow with confirmation.

    Task ID: T025 - Implement delete_task_flow in main.py to handle the complete delete task workflow with confirmation
    """
    try:
        task_id = get_task_id("Enter the ID of the task to delete: ")
        if task_id is None:
            display_error("Invalid task ID.")
            return

        # Check if task exists
        task = task_manager.get_task(task_id)
        if task is None:
            display_error(f"Task with ID {task_id} not found.")
            return

        print(f"\nTask to delete: {task.title}")
        print(f"Description: {task.description}")

        if get_confirmation():
            success = task_manager.delete_task(task_id)
            if success:
                display_success(f"Task {task_id} deleted successfully.")
            else:
                display_error(f"Failed to delete task {task_id}.")
        else:
            display_info("Deletion cancelled.")
    except Exception as e:
        display_error(f"Failed to delete task: {str(e)}")


def toggle_complete_flow(task_manager: TaskManager):
    """
    Handle the complete toggle complete/incomplete workflow.

    Task ID: T022 - Implement toggle_complete_flow in main.py to handle the complete complete/incomplete toggle workflow
    """
    try:
        task_id = get_task_id("Enter the ID of the task to toggle: ")
        if task_id is None:
            display_error("Invalid task ID.")
            return

        # Check if task exists
        task = task_manager.get_task(task_id)
        if task is None:
            display_error(f"Task with ID {task_id} not found.")
            return

        success = task_manager.toggle_task_completion(task_id)
        if success:
            new_status = "completed" if task.completed else "incomplete"
            display_success(f"Task {task_id} marked as {new_status}.")
        else:
            display_error(f"Failed to toggle completion status for task {task_id}.")
    except Exception as e:
        display_error(f"Failed to toggle task completion: {str(e)}")


if __name__ == "__main__":
    main()
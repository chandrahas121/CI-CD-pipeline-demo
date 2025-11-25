import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


DATA_FILE = Path("todos.json")


@dataclass
class Todo:
    id: int
    title: str
    done: bool = False


def _load_todos() -> List[Todo]:
    if not DATA_FILE.exists():
        return []
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Todo(**item) for item in raw]


def _save_todos(todos: List[Todo]) -> None:
    DATA_FILE.write_text(
        json.dumps([asdict(t) for t in todos], indent=2),
        encoding="utf-8",
    )


def add_todo(title: str) -> Todo:
    todos = _load_todos()
    next_id = (max((t.id for t in todos), default=0) + 1)
    todo = Todo(id=next_id, title=title, done=False)
    todos.append(todo)
    _save_todos(todos)
    return todo


def list_todos() -> List[Todo]:
    return _load_todos()


def complete_todo(todo_id: int) -> bool:
    todos = _load_todos()
    for t in todos:
        if t.id == todo_id:
            t.done = True
            _save_todos(todos)
            return True
    return False


def delete_todo(todo_id: int) -> bool:
    todos = _load_todos()
    new_todos = [t for t in todos if t.id != todo_id]
    if len(new_todos) == len(todos):
        return False
    _save_todos(new_todos)
    return True


def _print_todos(todos: List[Todo]) -> None:
    if not todos:
        print("No tasks yet.")
        return
    for t in todos:
        status = "[x]" if t.done else "[ ]"
        print(f"{t.id}. {status} {t.title}")


def main() -> None:
    while True:
        print("\nTo-Do List")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            if title:
                todo = add_todo(title)
                print(f"Added task #{todo.id}: {todo.title}")
            else:
                print("Title cannot be empty.")
        elif choice == "2":
            _print_todos(list_todos())
        elif choice == "3":
            try:
                todo_id = int(input("Task id to complete: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            if complete_todo(todo_id):
                print("Task marked as done.")
            else:
                print("Task not found.")
        elif choice == "4":
            try:
                todo_id = int(input("Task id to delete: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            if delete_todo(todo_id):
                print("Task deleted.")
            else:
                print("Task not found.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()

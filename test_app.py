import json
from pathlib import Path

import app


def setup_function(_):
    data_file = Path("todos.json")
    if data_file.exists():
        data_file.unlink()


def test_add_and_list_todo():
    todo = app.add_todo("Write tests")
    assert todo.id == 1
    assert todo.title == "Write tests"
    assert todo.done is False

    todos = app.list_todos()
    assert len(todos) == 1
    assert todos[0].title == "Write tests"


def test_complete_todo():
    todo = app.add_todo("Finish homework")
    assert not todo.done

    ok = app.complete_todo(todo.id)
    assert ok is True

    todos = app.list_todos()
    assert todos[0].done is True


def test_delete_todo():
    t1 = app.add_todo("Task 1")
    t2 = app.add_todo("Task 2")

    ok = app.delete_todo(t1.id)
    assert ok is True

    titles = [t.title for t in app.list_todos()]
    assert titles == ["Task 2"]

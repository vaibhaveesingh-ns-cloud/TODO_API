#In-memory DB
from typing import Dict
from models import TodoCreate, TodoUpdate, TodoResponse

# Simulating database with dictionary
db: Dict[int, TodoResponse] = {}
counter = 0

def create(todo: TodoCreate) -> TodoResponse:
    global counter
    counter += 1
    new_todo = TodoResponse(id=counter, **todo.dict())
    db[counter] = new_todo
    return new_todo

def get_all() -> list[TodoResponse]:
    return list(db.values())

def get_by_id(todo_id: int) -> TodoResponse | None:
    return db.get(todo_id)

def update(todo_id: int, data: TodoUpdate) -> TodoResponse | None:
    if todo_id not in db:
        return None
    stored = db[todo_id]
    updated = stored.copy(update=data.dict(exclude_unset=True))
    db[todo_id] = updated
    return updated

def delete(todo_id: int) -> bool:
    return db.pop(todo_id, None) is not None

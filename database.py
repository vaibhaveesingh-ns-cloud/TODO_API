from typing import Dict, List, Optional
from models import TodoCreate, TodoUpdate, TodoResponse

# Simulating database with a dictionary
db: Dict[int, TodoResponse] = {}
counter = 0

def create(todo: TodoCreate, owner_id: int) -> TodoResponse:
    global counter
    counter += 1
    new_todo = TodoResponse(id=counter, owner_id=owner_id, **todo.dict())
    db[counter] = new_todo
    return new_todo

def get_all_for_user(owner_id: int) -> List[TodoResponse]:
    return [t for t in db.values() if t.owner_id == owner_id]

def get_by_id(todo_id: int) -> Optional[TodoResponse]:
    return db.get(todo_id)

def update(todo_id: int, data: TodoUpdate) -> Optional[TodoResponse]:
    if todo_id not in db:
        return None
    stored = db[todo_id]
    updated = stored.copy(update=data.dict(exclude_unset=True))
    db[todo_id] = updated
    return updated

def delete(todo_id: int) -> bool:
    return db.pop(todo_id, None) is not None

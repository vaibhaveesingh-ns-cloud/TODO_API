from fastapi import FastAPI, HTTPException, Depends
from models import TodoCreate, TodoUpdate, TodoResponse
import database
from middleware import log_requests
from auth import router as auth_router, get_current_user

app = FastAPI(title="Todo API with JWT Auth", version="1.1.0")

# Add Middleware
app.middleware("http")(log_requests)

# Include auth routes
app.include_router(auth_router)

# Protected Todo routes
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, current_user: dict = Depends(get_current_user)):
    return database.create(todo, owner_id=current_user["id"])

@app.get("/todos/", response_model=list[TodoResponse])
def list_todos(current_user: dict = Depends(get_current_user)):
    return database.get_all_for_user(owner_id=current_user["id"])

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    todo = database.get_by_id(todo_id)
    if not todo or todo.owner_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, current_user: dict = Depends(get_current_user)):
    stored = database.get_by_id(todo_id)
    if not stored or stored.owner_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated = database.update(todo_id, todo)
    return updated

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user: dict = Depends(get_current_user)):
    stored = database.get_by_id(todo_id)
    if not stored or stored.owner_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Todo not found")
    success = database.delete(todo_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete")
    return {"message": "Todo deleted successfully"}

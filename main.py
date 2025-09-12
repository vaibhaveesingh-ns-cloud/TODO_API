# Entry point for the application
from fastapi import FastAPI, HTTPException
from models import TodoCreate, TodoUpdate, TodoResponse
import database
from middleware import log_requests

app = FastAPI(title="Todo API", version="1.0.0")

# Add Middleware
app.middleware("http")(log_requests)

# Routes
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    return database.create(todo)

@app.get("/todos/", response_model=list[TodoResponse])
def list_todos():
    return database.get_all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    todo = database.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    updated = database.update(todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    success = database.delete(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

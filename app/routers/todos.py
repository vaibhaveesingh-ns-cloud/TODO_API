from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, auth

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=models.TodoOut)
def create_todo(todo_in: models.TodoCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return crud.create_todo(db, current_user.id, todo_in.title, todo_in.description or "")

@router.get("/", response_model=list[models.TodoOut])
def list_todos(db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return crud.get_todos_for_user(db, current_user.id)

@router.get("/{todo_id}", response_model=models.TodoOut)
def get_todo(todo_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    todo = crud.get_todo_by_id(db, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=models.TodoOut)
def update_todo(todo_id: int, todo_in: models.TodoCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    todo = crud.get_todo_by_id(db, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return crud.update_todo(db, todo, title=todo_in.title, description=todo_in.description)

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    todo = crud.get_todo_by_id(db, todo_id)
    if not todo or todo.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    crud.delete_todo(db, todo)
    return {"message": "Deleted"}

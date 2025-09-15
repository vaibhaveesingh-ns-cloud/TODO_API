from sqlalchemy.orm import Session
from . import models
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User helpers
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str) -> models.User:
    hashed = pwd_context.hash(password)
    user = models.User(username=username, email=email, hashed_password=hashed, is_active=False, is_admin=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def activate_user(db: Session, user: models.User):
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user

def promote_user_to_admin(db: Session, user: models.User):
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return user

# Todo helpers
def create_todo(db: Session, owner_id: int, title: str, description: str):
    todo = models.Todo(title=title, description=description, owner_id=owner_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_todos_for_user(db: Session, owner_id: int):
    return db.query(models.Todo).filter(models.Todo.owner_id == owner_id).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def update_todo(db: Session, todo: models.Todo, **fields):
    for k, v in fields.items():
        setattr(todo, k, v)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo: models.Todo):
    db.delete(todo)
    db.commit()
    return True

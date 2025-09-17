from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..database import get_db
from .. import crud, models, auth
from typing import Optional, List
from datetime import datetime, timedelta

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Get dashboard statistics for admin overview"""
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.is_active == True).count()
    admin_users = db.query(models.User).filter(models.User.is_admin == True).count()
    total_todos = db.query(models.Todo).count()
    completed_todos = db.query(models.Todo).filter(models.Todo.completed == True).count()
    
    # Recent activity (users created in last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_users = db.query(models.User).filter(models.User.created_at >= week_ago).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "admin_users": admin_users,
        "inactive_users": total_users - active_users,
        "total_todos": total_todos,
        "completed_todos": completed_todos,
        "pending_todos": total_todos - completed_todos,
        "recent_users": recent_users,
        "completion_rate": round((completed_todos / total_todos * 100) if total_todos > 0 else 0, 1)
    }

@router.get("/users", response_model=list[models.UserOut])
def list_users(db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """List all users with their basic information"""
    return db.query(models.User).order_by(desc(models.User.created_at)).all()

@router.get("/users/{user_id}/todos", response_model=list[models.TodoOut])
def get_user_todos(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Get all todos for a specific user"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).order_by(desc(models.Todo.created_at)).all()

@router.get("/todos")
def get_all_todos(
    db: Session = Depends(get_db), 
    admin=Depends(auth.get_current_active_admin),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(100, description="Limit number of results"),
    offset: int = Query(0, description="Offset for pagination")
):
    """Get all todos across all users with filtering options"""
    query = db.query(models.Todo, models.User).join(models.User, models.Todo.owner_id == models.User.id)
    
    if user_id:
        query = query.filter(models.Todo.owner_id == user_id)
    
    if completed is not None:
        query = query.filter(models.Todo.completed == completed)
    
    query = query.order_by(desc(models.Todo.created_at))
    todos_with_users = query.offset(offset).limit(limit).all()
    
    result = []
    for todo, user in todos_with_users:
        result.append({
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "owner_id": todo.owner_id,
            "created_at": todo.created_at,
            "owner_username": user.username,
            "owner_email": user.email
        })
    
    return {
        "todos": result,
        "total": db.query(models.Todo).count(),
        "filtered_count": len(result)
    }

@router.get("/users/detailed")
def get_users_with_stats(db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Get users with their todo statistics"""
    users = db.query(models.User).all()
    result = []
    
    for user in users:
        todo_count = db.query(models.Todo).filter(models.Todo.owner_id == user.id).count()
        completed_count = db.query(models.Todo).filter(
            models.Todo.owner_id == user.id, 
            models.Todo.completed == True
        ).count()
        
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "created_at": user.created_at,
            "todo_count": todo_count,
            "completed_count": completed_count,
            "pending_count": todo_count - completed_count,
            "completion_rate": round((completed_count / todo_count * 100) if todo_count > 0 else 0, 1)
        })
    
    return sorted(result, key=lambda x: x["created_at"], reverse=True)

@router.post("/users/{user_id}/promote", response_model=models.UserOut)
def promote_user(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Promote a user to admin status"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.promote_user_to_admin(db, user)

@router.post("/users/{user_id}/demote", response_model=models.UserOut)
def demote_user(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Remove admin status from a user"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = False
    db.commit()
    db.refresh(user)
    return user

@router.post("/users/{user_id}/activate", response_model=models.UserOut)
def activate_user(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Activate a user account"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user

@router.post("/users/{user_id}/deactivate", response_model=models.UserOut)
def deactivate_user(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Deactivate a user account"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Delete a user and all their todos"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user (todos will be deleted automatically due to cascade)
    db.delete(user)
    db.commit()
    return {"message": f"User {user.username} and all their todos have been deleted"}

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    """Delete a specific todo"""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

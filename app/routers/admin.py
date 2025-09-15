from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models, auth

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[models.UserOut])
def list_users(db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    return db.query(models.User).all()

@router.post("/users/{user_id}/promote", response_model=models.UserOut)
def promote_user(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.promote_user_to_admin(db, user)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin=Depends(auth.get_current_active_admin)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

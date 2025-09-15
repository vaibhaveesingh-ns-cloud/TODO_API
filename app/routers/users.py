from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, crud, auth, email_utils
from ..database import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str

@router.post("/register", response_model=RegisterResponse)
def register(user_in: models.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username) or crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    user = crud.create_user(db, user_in.username, user_in.email, user_in.password)
    token = email_utils.generate_verification_token(user.email)
    email_utils.send_verification_email(user.email, token)
    return {"id": user.id, "username": user.username, "email": user.email}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = email_utils.confirm_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.activate_user(db, user)
    return {"message": "Email verified. You can now login."}

@router.post("/token", response_model=models.Token)
def login_for_token(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Note: OAuth2PasswordRequestForm is in fastapi.security
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

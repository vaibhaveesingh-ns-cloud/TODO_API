from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import crud, models
from .database import get_db
from .rate_limit import RateLimiter, SessionManager, get_client_ip, get_user_agent
from pydantic import BaseModel
from typing import Optional

# secrets - use env vars in prod
SECRET_KEY = "CHANGE_ME_LONG_RANDOM"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return None
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(*, data: dict, session_token: str, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire, 
        "iat": datetime.utcnow(),
        "session_token": session_token
    })
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded

def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    # First validate JWT token structure
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        session_token: str = payload.get("session_token")
        if username is None or session_token is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Validate session
    session = SessionManager.validate_session(db, session_token)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                          detail="Session expired or invalid")
    
    # Get user
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User email not verified")
    
    # Verify session belongs to user
    if session.user_id != user.id:
        raise credentials_exception
    
    return user

def get_current_active_admin(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


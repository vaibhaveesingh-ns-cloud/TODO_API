from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import UserCreate, TokenData
from fastapi import APIRouter
from pydantic import BaseModel

# Secret key — in production load from env variable
SECRET_KEY = "CHANGE_THIS_TO_A_RANDOM_SECURE_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Simple in-memory user "db" for demo; replace with real DB later
# structure: username -> {"id": int, "username": str, "hashed_password": str}
users_db: dict[str, dict] = {}
_user_counter = 0

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(user: UserCreate) -> dict:
    global _user_counter
    if user.username in users_db:
        raise ValueError("Username already exists")
    _user_counter += 1
    users_db[user.username] = {
        "id": _user_counter,
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
    }
    return users_db[user.username]

def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": now})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Router for auth endpoints
router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterResponse(BaseModel):
    id: int
    username: str

@router.post("/register", response_model=RegisterResponse)
def register(user: UserCreate):
    try:
        created = create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"id": created["id"], "username": created["username"]}

@router.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

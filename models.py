from pydantic import BaseModel, Field
from typing import Optional

# Auth models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# Todo models
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=250)
    completed: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=250)
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    owner_id: int

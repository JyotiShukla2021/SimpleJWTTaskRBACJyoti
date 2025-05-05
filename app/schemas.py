from pydantic import BaseModel
from typing import Optional
from models import RoleEnum

class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

from sqlmodel import SQLModel, Field
from typing import Optional
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    user = "user"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: RoleEnum

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]

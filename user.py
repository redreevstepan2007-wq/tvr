from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    ANALYST = "analyst"

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str
    birth_date: Optional[date] = None
    hashed_password: str
    role: UserRole = Field(default=UserRole.OPERATOR)
    is_active: bool = Field(default=True)
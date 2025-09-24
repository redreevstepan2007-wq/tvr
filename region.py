from sqlmodel import SQLModel, Field
from typing import Optional

class Region(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    code: str = Field(unique=True)  # Код региона

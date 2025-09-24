from sqlmodel import SQLModel, Field

class DeathReason(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True, unique=True)
    code: str = Field(unique=True)  # Медицинский код причины смерти
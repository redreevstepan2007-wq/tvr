from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class PersonBase(SQLModel):
    last_name: str
    first_name: str
    patronymic: Optional[str] = None
    gender: Gender
    birth_date: date
    birth_region_id: int = Field(foreign_key="region.id")

class Newborn(PersonBase, table=True):
    id: int = Field(primary_key=True)
    # Сведения о родителях
    mother_last_name: str
    mother_first_name: str
    mother_patronymic: Optional[str] = None
    mother_birth_date: date
    father_last_name: Optional[str] = None
    father_first_name: Optional[str] = None
    father_patronymic: Optional[str] = None
    father_birth_date: Optional[date] = None

class Deceased(PersonBase, table=True):
    id: int = Field(primary_key=True)
    death_date: date
    death_region_id: int = Field(foreign_key="region.id")
    death_reason_id: int = Field(foreign_key="deathreason.id")
    death_certificate_number: Optional[str] = None
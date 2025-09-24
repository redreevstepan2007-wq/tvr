from typing import Optional, List
from sqlmodel import Session, select
from db.database import engine
from models.person import Newborn
from models.region import Region
from datetime import date

def add_newborn(
    last_name: str,
    first_name: str,
    patronymic: Optional[str],
    gender: str,
    birth_date: date,
    birth_region_id: int,
    mother_last_name: str,
    mother_first_name: str,
    mother_patronymic: Optional[str],
    mother_birth_date: date,
    father_last_name: Optional[str] = None,
    father_first_name: Optional[str] = None,
    father_patronymic: Optional[str] = None,
    father_birth_date: Optional[date] = None
) -> Optional[Newborn]:
    
    with Session(engine) as session:
        # Проверяем существование региона
        region = session.get(Region, birth_region_id)
        if not region:
            return None
            
        newborn = Newborn(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            gender=gender,
            birth_date=birth_date,
            birth_region_id=birth_region_id,
            mother_last_name=mother_last_name,
            mother_first_name=mother_first_name,
            mother_patronymic=mother_patronymic,
            mother_birth_date=mother_birth_date,
            father_last_name=father_last_name,
            father_first_name=father_first_name,
            father_patronymic=father_patronymic,
            father_birth_date=father_birth_date
        )
        
        session.add(newborn)
        session.commit()
        session.refresh(newborn)
        return newborn

def get_newborns(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region_id: Optional[int] = None
) -> List[Newborn]:
    
    with Session(engine) as session:
        query = select(Newborn)
        
        if start_date:
            query = query.where(Newborn.birth_date >= start_date)
        if end_date:
            query = query.where(Newborn.birth_date <= end_date)
        if region_id:
            query = query.where(Newborn.birth_region_id == region_id)
            
        newborns = session.exec(query).all()
        return newborns
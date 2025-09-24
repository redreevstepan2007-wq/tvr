from typing import Optional, List
from sqlmodel import Session, select
from db.database import engine
from models.person import Deceased
from models.region import Region
from models.death_reason import DeathReason
from datetime import date

def add_deceased(
    last_name: str,
    first_name: str,
    patronymic: Optional[str],
    gender: str,
    birth_date: date,
    birth_region_id: int,
    death_date: date,
    death_region_id: int,
    death_reason_id: int,
    death_certificate_number: Optional[str] = None
) -> Optional[Deceased]:
    
    with Session(engine) as session:
        # Проверяем существование регионов и причины смерти
        birth_region = session.get(Region, birth_region_id)
        death_region = session.get(Region, death_region_id)
        death_reason = session.get(DeathReason, death_reason_id)
        
        if not all([birth_region, death_region, death_reason]):
            return None
            
        deceased = Deceased(
            last_name=last_name,
            first_name=first_name,
            patronymic=patronymic,
            gender=gender,
            birth_date=birth_date,
            birth_region_id=birth_region_id,
            death_date=death_date,
            death_region_id=death_region_id,
            death_reason_id=death_reason_id,
            death_certificate_number=death_certificate_number
        )
        
        session.add(deceased)
        session.commit()
        session.refresh(deceased)
        return deceased

def get_deceased(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    region_id: Optional[int] = None,
    death_reason_id: Optional[int] = None
) -> List[Deceased]:
    
    with Session(engine) as session:
        query = select(Deceased)
        
        if start_date:
            query = query.where(Deceased.death_date >= start_date)
        if end_date:
            query = query.where(Deceased.death_date <= end_date)
        if region_id:
            query = query.where(Deceased.death_region_id == region_id)
        if death_reason_id:
            query = query.where(Deceased.death_reason_id == death_reason_id)
            
        deceased = session.exec(query).all()
        return deceased
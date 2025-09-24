from typing import Dict, List, Tuple
from sqlmodel import Session, select, func
from db.database import engine
from models.person import Newborn, Deceased, Gender
from models.region import Region
from models.death_reason import DeathReason
from datetime import date
from collections import defaultdict

def get_demographic_statistics(
    start_date: date,
    end_date: date
) -> Dict:
    """
    Получение демографической статистики за период
    """
    with Session(engine) as session:
        # Статистика по новорожденным
        newborns_query = select(Newborn).where(
            Newborn.birth_date >= start_date,
            Newborn.birth_date <= end_date
        )
        newborns = session.exec(newborns_query).all()
        
        # Статистика по умершим
        deceased_query = select(Deceased).where(
            Deceased.death_date >= start_date,
            Deceased.death_date <= end_date
        )
        deceased = session.exec(deceased_query).all()
        
        # Анализ по полу среди новорожденных
        newborn_gender_stats = defaultdict(int)
        for newborn in newborns:
            newborn_gender_stats[newborn.gender] += 1
        
        # Анализ по полу среди умерших
        deceased_gender_stats = defaultdict(int)
        for person in deceased:
            deceased_gender_stats[person.gender] += 1
        
        # Анализ причин смерти
        death_reasons_stats = defaultdict(int)
        for person in deceased:
            death_reason = session.get(DeathReason, person.death_reason_id)
            if death_reason:
                death_reasons_stats[death_reason.name] += 1
        
        return {
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "newborns": {
                "total": len(newborns),
                "by_gender": dict(newborn_gender_stats),
                "male_female_ratio": (
                    newborn_gender_stats[Gender.MALE] / len(newborns) * 100 
                    if newborns else 0,
                    newborn_gender_stats[Gender.FEMALE] / len(newborns) * 100 
                    if newborns else 0
                )
            },
            "deceased": {
                "total": len(deceased),
                "by_gender": dict(deceased_gender_stats),
                "death_reasons": dict(death_reasons_stats)
            },
            "natural_increase": len(newborns) - len(deceased)  # Естественный прирост
        }
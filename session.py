from sqlmodel import Session
from db.database import engine

def get_session():
    """
    Возврат объектов сессии туда, откуда сессия была вызвана
    :return:
    """
    with Session(engine) as session:
        yield session
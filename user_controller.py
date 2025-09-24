from typing import Optional
from sqlmodel import Session, select
from db.database import engine
from models.user import User, UserRole
from datetime import date
from argon2 import PasswordHasher, exceptions as argon2_exceptions

def add_user(
    username: str,
    email: str,
    full_name: str,
    password: str,
    role: UserRole = UserRole.OPERATOR,
    birth_date: Optional[date] = None
) -> Optional[User]:
    
    ph = PasswordHasher()
    hash_pass = ph.hash(password)

    with Session(engine) as session:
        # Проверяем уникальность email и username
        existing_user = session.exec(
            select(User).where(
                (User.email == email) | (User.username == username)
            )
        ).first()
        
        if existing_user:
            return None
            
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            birth_date=birth_date,
            hashed_password=hash_pass,
            role=role
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def authenticate_user(email: str, password: str) -> Optional[User]:
    ph = PasswordHasher()
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if user is None or not user.is_active:
            return None
        try:
            ph.verify(user.hashed_password, password)
            return user
        except argon2_exceptions.VerifyMismatchError:
            return None

def list_users() -> list[User]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

def find_user(id_user: int) -> Optional[User]:
    with Session(engine) as session:
        user = session.get(User, id_user)
        return user

def edit_user(
    id_user: int,
    new_email: Optional[str] = None,
    new_username: Optional[str] = None,
    new_full_name: Optional[str] = None,
    new_role: Optional[UserRole] = None,
    is_active: Optional[bool] = None
) -> Optional[User]:
    
    with Session(engine) as session:
        user = session.get(User, id_user)
        if user:
            if new_email is not None:
                user.email = new_email
            if new_username is not None:
                user.username = new_username
            if new_full_name is not None:
                user.full_name = new_full_name
            if new_role is not None:
                user.role = new_role
            if is_active is not None:
                user.is_active = is_active
                
            session.commit()
            session.refresh(user)
            return user
    return None

def delete_user(id_user: int) -> bool:
    with Session(engine) as session:
        user = session.get(User, id_user)
        if user:
            session.delete(user)
            session.commit()
        user = session.get(User, id_user)
        return user is None
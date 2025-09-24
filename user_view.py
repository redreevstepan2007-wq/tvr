from models.user import User
from models.person import Newborn, Deceased
from typing import Optional, List
from datetime import date

def show_users(arr_users: List[User]):
    """
    Вывод на экран информации о пользователях
    """
    print("\n=== СПИСОК ПОЛЬЗОВАТЕЛЕЙ ===")
    for user in arr_users:
        print(f"ID: {user.id}, Имя: {user.username}, Email: {user.email}, Роль: {user.role}")

def show_newborns(newborns: List[Newborn]):
    """
    Вывод на экран информации о новорожденных
    """
    print("\n=== СПИСОК НОВОРОЖДЕННЫХ ===")
    for newborn in newborns:
        print(f"ID: {newborn.id}, ФИО: {newborn.last_name} {newborn.first_name} {newborn.patronymic or ''}, "
              f"Пол: {newborn.gender}, Дата рождения: {newborn.birth_date}")

def show_deceased(deceased: List[Deceased]):
    """
    Вывод на экран информации об умерших
    """
    print("\n=== СПИСОК УМЕРШИХ ===")
    for person in deceased:
        print(f"ID: {person.id}, ФИО: {person.last_name} {person.first_name} {person.patronymic or ''}, "
              f"Дата рождения: {person.birth_date}, Дата смерти: {person.death_date}")

def input_user_id():
    """
    Запрос информации об идентификаторе пользователя
    """
    try:
        id = int(input("Введите идентификатор пользователя: "))
        return id
    except Exception:
        print("Ошибка ввода идентификатора")
        return None

def input_newborn_data():
    """
    Ввод данных о новорожденном
    """
    print("\n=== ВВОД ДАННЫХ О НОВОРОЖДЕННОМ ===")
    last_name = input("Фамилия: ")
    first_name = input("Имя: ")
    patronymic = input("Отчество (если есть): ") or None
    gender = input("Пол (male/female): ")
    birth_date_str = input("Дата рождения (ГГГГ-ММ-ДД): ")
    
    # Данные о матери
    mother_last_name = input("Фамилия матери: ")
    mother_first_name = input("Имя матери: ")
    mother_patronymic = input("Отчество матери: ") or None
    mother_birth_date_str = input("Дата рождения матери (ГГГГ-ММ-ДД): ")
    
    # Данные об отце (опционально)
    father_last_name = input("Фамилия отца (если есть): ") or None
    father_first_name = input("Имя отца (если есть): ") or None
    father_patronymic = input("Отчество отца (если есть): ") or None
    father_birth_date_str = input("Дата рождения отца (ГГГГ-ММ-ДД, если есть): ") or None
    
    try:
        birth_date = date.fromisoformat(birth_date_str)
        mother_birth_date = date.fromisoformat(mother_birth_date_str)
        father_birth_date = date.fromisoformat(father_birth_date_str) if father_birth_date_str else None
        
        return {
            "last_name": last_name,
            "first_name": first_name,
            "patronymic": patronymic,
            "gender": gender,
            "birth_date": birth_date,
            "birth_region_id": 1,  # По умолчанию
            "mother_last_name": mother_last_name,
            "mother_first_name": mother_first_name,
            "mother_patronymic": mother_patronymic,
            "mother_birth_date": mother_birth_date,
            "father_last_name": father_last_name,
            "father_first_name": father_first_name,
            "father_patronymic": father_patronymic,
            "father_birth_date": father_birth_date
        }
    except ValueError:
        print("Ошибка формата даты")
        return None

def show_result_auth(data: Optional[User]):
    """
    Показать результат авторизации
    """
    if data is None:
        print(" Вы не авторизованы")
    else:
        print(f"Авторизация прошла успешно! Добро пожаловать, {data.username} ({data.role})")

def show_demographic_statistics(stats: dict):
    """
    Показать демографическую статистику
    """
    print("\n=== ДЕМОГРАФИЧЕСКАЯ СТАТИСТИКА ===")
    print(f"Период: {stats['period']['start_date']} - {stats['period']['end_date']}")
    print(f"Новорожденные: {stats['newborns']['total']}")
    print(f"Умершие: {stats['deceased']['total']}")
    print(f"Естественный прирост: {stats['natural_increase']}")
    
    if stats['newborns']['total'] > 0:
        print(f"Соотношение полов новорожденных: {stats['newborns']['by_gender']}")
    
    if stats['deceased']['total'] > 0:
        print(f"Соотношение полов умерших: {stats['deceased']['by_gender']}")
        print(f"Основные причины смерти: {stats['deceased']['death_reasons']}")
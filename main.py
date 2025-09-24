from controllers.user_controller import list_users, authenticate_user, add_user
from controllers.newborn_controller import add_newborn, get_newborns
from controllers.deceased_controller import add_deceased, get_deceased
from controllers.analytics_controller import get_demographic_statistics
from db.database import init_db
from views.user_view import (show_users, show_newborns, show_deceased, 
                               show_result_auth, input_newborn_data, show_demographic_statistics)
from datetime import date, timedelta

def main():
    # Инициализация базы данных
    init_db()
    
    print("=== СИСТЕМА УЧЕТА ДЕМОГРАФИЧЕСКОЙ СИТУАЦИИ ===")
    
    # Создаем тестового пользователя
    test_user = add_user(
        username="admin",
        email="admin@demography.ru",
        full_name="Администратор системы",
        password="admin123",
        role="admin"
    )
    
    if test_user:
        print(" Тестовый пользователь создан")
    
    # Авторизация
    print("\n--- АВТОРИЗАЦИЯ ---")
    result = authenticate_user("admin@demography.ru", "admin123")
    show_result_auth(result)
    
    if result:
        # Показываем пользователей
        users = list_users()
        show_users(users)
        
        # Демонстрация работы с новорожденными
        print("\n--- РАБОТА С ДЕМОГРАФИЧЕСКИМИ ДАННЫМИ ---")
        
        # Добавляем тестового новорожденного
        newborn_data = {
            "last_name": "Иванов",
            "first_name": "Петр",
            "patronymic": "Сергеевич",
            "gender": "male",
            "birth_date": date(2024, 1, 15),
            "birth_region_id": 1,
            "mother_last_name": "Иванова",
            "mother_first_name": "Мария",
            "mother_patronymic": "Владимировна",
            "mother_birth_date": date(1990, 5, 20),
            "father_last_name": "Иванов",
            "father_first_name": "Сергей",
            "father_patronymic": "Петрович",
            "father_birth_date": date(1988, 3, 10)
        }
        
        newborn = add_newborn(**newborn_data)
        if newborn:
            print("Тестовый новорожденный добавлен")
        
        # Добавляем тестового умершего
        deceased_data = {
            "last_name": "Петров",
            "first_name": "Иван",
            "patronymic": "Михайлович",
            "gender": "male",
            "birth_date": date(1950, 7, 10),
            "birth_region_id": 1,
            "death_date": date(2024, 1, 20),
            "death_region_id": 1,
            "death_reason_id": 1
        }
        
        deceased = add_deceased(**deceased_data)
        if deceased:
            print("Тестовый умерший добавлен")
        
        # Показываем демографические данные
        newborns = get_newborns()
        show_newborns(newborns)
        
        deceased_list = get_deceased()
        show_deceased(deceased_list)
        
        # Демонстрация аналитики
        print("\n--- АНАЛИТИКА ДЕМОГРАФИЧЕСКОЙ СИТУАЦИИ ---")
        end_date = date.today()
        start_date = end_date - timedelta(days=365)  # За последний год
        
        stats = get_demographic_statistics(start_date, end_date)
        show_demographic_statistics(stats)
        
        # Пример интерактивного ввода
        print("\n--- ИНТЕРАКТИВНЫЙ ВВОД ДАННЫХ ---")
        print("Для выхода введите 'exit'")
        
        while True:
            command = input("\nВведите команду (newborn - добавить новорожденного, exit - выход): ")
            
            if command == "exit":
                break
            elif command == "newborn":
                newborn_data = input_newborn_data()
                if newborn_data:
                    newborn = add_newborn(**newborn_data)
                    if newborn:
                        print(" Новорожденный успешно добавлен!")
                    else:
                        print(" Ошибка при добавлении новорожденного")
            else:
                print(" Неизвестная команда")

if __name__ == "__main__":
    main()
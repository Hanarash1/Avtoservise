# Функция для загрузки пользователей из текстового файла
def load_users():
    try:
        with open('users.txt', 'r') as f:
            lines = f.readlines()
            users = []
            for line in lines:
                username, password, role = line.strip().split(',')  # Разделяем строку по запятой
                users.append({'username': username, 'password': password, 'role': role, 'history': []})
    except FileNotFoundError:
        # Если файл не найден, создаем его и добавляем начальных пользователей
        print("Файл с пользователями не найден. Создаем новый файл.")
        users = [
            {'username': 'user', 'password': 'user1', 'role': 'user', 'history': []},
            {'username': 'admin', 'password': 'admin1', 'role': 'admin', 'history': []}
        ]
        save_users(users)  # Сохраняем начальных пользователей в файл
    return users

# Функция для сохранения пользователей в текстовый файл
def save_users(users):
    with open('users.txt', 'w') as f:
        for user in users:
            # Сохраняем данные пользователя в виде строки с разделением запятой
            f.write(f"{user['username']},{user['password']},{user['role']}\n")

# Функция для логина
def login(users):
    username = input('Логин: ')
    password = input('Пароль: ')
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    print('Неверный логин или пароль.')
    return None

# Функция для отображения доступных услуг
def show_services(services):
    print("\nДоступные услуги:")
    print(f"{'№':<4}{'Услуга':<20}{'Стоимость':<10}")
    for i, service in enumerate(services, 1):
        print(f"{i:<4}{service['name']:<20}{service['cost']:<10}")

# Функция для сортировки услуг
def sort_services(services):
    print("Сортировка услуг:")
    print("1. По стоимости")
    print("2. По названию")
    choice = input("Выберите критерий сортировки: ")
    
    if choice == '1':
        sorted_services = sorted(services, key=lambda x: x['cost'])
    elif choice == '2':
        sorted_services = sorted(services, key=lambda x: x['name'])
    else:
        print("Неверный выбор.")
        return services
    show_services(sorted_services)
    return sorted_services

# Функция для фильтрации услуг
def filter_services(services):
    print("Фильтрация услуг:")
    min_cost = input("Введите минимальную стоимость (или нажмите Enter для пропуска): ")
    max_cost = input("Введите максимальную стоимость (или нажмите Enter для пропуска): ")
    
    try:
        if min_cost:
            min_cost = float(min_cost)
        else:
            min_cost = 0
        if max_cost:
            max_cost = float(max_cost)
        else:
            max_cost = float('inf')
    except ValueError:
        print("Ошибка: Стоимость должна быть числом.")
        return services

    filtered_services = filter(lambda x: min_cost <= x['cost'] <= max_cost, services)
    filtered_services = list(filtered_services)
    show_services(filtered_services)
    return filtered_services

# Функция для записи на услугу
def book_service(user, services):
    while True:
        try:
            show_services(services)
            service_choice = int(input('Выберите услугу для записи (номер): ')) - 1
            if 0 <= service_choice < len(services):
                service = services[service_choice]
                user['history'].append({'service': service['name'], 'cost': service['cost'], 'date': '2024-12-05'})
                print(f"Вы записались на услугу {service['name']}")
                break
            else:
                print('Неверный выбор услуги. Пожалуйста, выберите корректный номер.')
        except ValueError:
            print("Ошибка: Введите число для выбора услуги.")

# Функция для отображения истории визитов пользователя
def show_history(user):
    if not user['history']:
        print("История визитов пуста.")
    else:
        print("История ваших визитов:")
        for entry in user['history']:
            print(f"Услуга: {entry['service']}, Стоимость: {entry['cost']} руб., Дата: {entry['date']}")

# Функция для обновления пароля пользователя
def update_profile(user, users):
    new_password = input('Введите новый пароль: ')
    user['password'] = new_password
    print(f'Пароль пользователя {user["username"]} успешно обновлен.')

    # Поскольку данные пользователей хранятся в списке users, обновим их в этом списке.
    for u in users:
        if u['username'] == user['username']:
            u['password'] = new_password
            break

    save_users(users)  # Сохраняем обновленные данные пользователей в файл
    print(f'Новый пароль для {user["username"]}: {new_password}')

# Функции для работы с админом

def admin_menu():
    print('\n1. Добавить услугу')
    print('2. Удалить услугу')
    print('3. Редактировать услугу')
    print('4. Управление пользователями')
    print('5. Просмотр статистики')
    print('6. Выйти')
    print('7. Добавить нового пользователя')
    print('8. Сортировать услуги')
    print('9. Фильтровать услуги')

def admin_add_service(services):
    while True:
        try:
            name = input('Введите название услуги: ')
            cost = float(input('Введите стоимость услуги: '))
            services.append({'name': name, 'cost': cost})
            print('Услуга добавлена.')
            break
        except ValueError:
            print("Ошибка: Стоимость должна быть числом.")

def admin_delete_service(services):
    while True:
        try:
            show_services(services)
            choice = int(input('Выберите услугу для удаления (номер): ')) - 1
            if 0 <= choice < len(services):
                del services[choice]
                print('Услуга удалена.')
                break
            else:
                print('Неверный выбор. Пожалуйста, выберите корректный номер.')
        except ValueError:
            print("Ошибка: Введите число для выбора услуги.")

def admin_edit_service(services):
    while True:
        try:
            show_services(services)
            choice = int(input('Выберите услугу для редактирования (номер): ')) - 1
            if 0 <= choice < len(services):
                name = input('Введите новое название услуги: ')
                cost = float(input('Введите новую стоимость услуги: '))
                services[choice] = {'name': name, 'cost': cost}
                print('Услуга обновлена.')
                break
            else:
                print('Неверный выбор. Пожалуйста, выберите корректный номер.')
        except ValueError:
            print("Ошибка: Введите число для выбора услуги.")

def admin_manage_users(users):
    print("Управление пользователями:")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user['username']} - {user['role']}")
    while True:
        try:
            choice = int(input('Выберите пользователя для редактирования (номер): ')) - 1
            if 0 <= choice < len(users):
                user = users[choice]
                print(f"Редактирование пользователя {user['username']}")
                new_role = input('Введите новую роль (user/admin): ')
                user['role'] = new_role
                print('Роль обновлена.')
                break
            else:
                print('Неверный выбор. Пожалуйста, выберите корректный номер.')
        except ValueError:
            print("Ошибка: Введите число для выбора пользователя.")

def admin_view_statistics(services):
    print("Статистика:")
    total_services = len(services)
    total_cost = sum(service['cost'] for service in services)
    print(f"Количество услуг: {total_services}")
    print(f"Общая стоимость услуг: {total_cost} руб.")

def admin_add_user(users):
    print("Добавление нового пользователя:")
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    role = input("Введите роль (user/admin): ")
    if role not in ['user', 'admin']:
        print("Ошибка: Роль должна быть либо 'user', либо 'admin'.")
        return
    users.append({'username': username, 'password': password, 'role': role, 'history': []})
    save_users(users)  # Сохраняем новых пользователей в файл
    print(f"Пользователь {username} с ролью {role} добавлен.")

def main():
    users = load_users()
    services = [
        {'name': 'Услуга 1', 'cost': 100},
        {'name': 'Услуга 2', 'cost': 200}
    ]

    while True:
        user = login(users)
        if user:
            if user['role'] == 'user':
                while True:
                    print("\n1. Просмотреть доступные услуги")
                    print("2. Записаться на услугу")
                    print("3. Просмотреть историю визитов")
                    print("4. Обновить профиль")
                    print("5. Выйти")
                    
                    choice = input("Выберите действие: ")
                    if choice == '1':
                        show_services(services)
                    elif choice == '2':
                        book_service(user, services)
                    elif choice == '3':
                        show_history(user)
                    elif choice == '4':
                        update_profile(user, users)
                    elif choice == '5':
                        break
                    else:
                        print("Неверный выбор.")
        
            elif user['role'] == 'admin':
                while True:
                    admin_menu()
                    choice = input("Выберите действие: ")
                    if choice == '1':
                        admin_add_service(services)
                    elif choice == '2':
                        admin_delete_service(services)
                    elif choice == '3':
                        admin_edit_service(services)
                    elif choice == '4':
                        admin_manage_users(users)
                    elif choice == '5':
                        admin_view_statistics(services)
                    elif choice == '6':
                        break
                    elif choice == '7':
                        admin_add_user(users)
                    elif choice == '8':
                        services = sort_services(services)
                    elif choice == '9':
                        services = filter_services(services)
                    else:
                        print("Неверный выбор.")
        else:
            print("Ошибка авторизации.")
            break

if __name__ == "__main__":
    main()

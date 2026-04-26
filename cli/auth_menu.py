from models.user import User
from models.restaurant import Restaurant, CUISINE_TYPES
from storage.user_storage import UserStorage
from storage.restaurant_storage import RestaurantStorage


class AuthMenu:
    def __init__(self, user_storage, restaurant_storage):
        self.user_storage = user_storage
        self.restaurant_storage = restaurant_storage

    def show(self):
        while True:
            print("\n" + "=" * 45)
            print("  Добро пожаловать в FoodDelivery")
            print("=" * 45)
            print("  1. Войти")
            print("  2. Зарегистрироваться как клиент или курьер")
            print("  3. Зарегистрировать ресторан")
            print("  0. Выйти из программы")
            print("-" * 45)

            choice = input("  Ваш выбор: ").strip()

            if choice == "1":
                user = self._login()
                if user:
                    return user
            elif choice == "2":
                self._register_user()
            elif choice == "3":
                self._register_restaurant()
            elif choice == "0":
                return None
            else:
                print("  [!] Неверный пункт. Попробуйте снова.")

    def _login(self):
        print("\n  --- Вход в систему ---")
        username = input("  Логин: ").strip()
        password = input("  Пароль: ").strip()

        user = self.user_storage.find_by_username(username)
        if user and user.password == password:
            print(f"  [✓] Вход выполнен! Роль: {user.role}")
            input("  Нажмите Enter для продолжения...")
            return user
        else:
            print("  [!] Неверный логин или пароль.")
            return None

    def _register_user(self):
        print("\n  --- Регистрация клиента / курьера ---")

        username = input("  Придумайте логин: ").strip()
        if not username:
            print("  [!] Логин не может быть пустым.")
            return
        if self.user_storage.exists(username):
            print("  [!] Пользователь с таким логином уже существует.")
            return

        password = input("  Придумайте пароль: ").strip()
        if not password:
            print("  [!] Пароль не может быть пустым.")
            return

        print("  Выберите роль:")
        print("    1. Клиент")
        print("    2. Курьер")
        role_choice = input("  Ваш выбор: ").strip()

        if role_choice == "1":
            role = "client"
        elif role_choice == "2":
            role = "courier"
        else:
            print("  [!] Неверный выбор роли.")
            return

        self.user_storage.save(User(username, password, role))
        print("  [✓] Регистрация прошла успешно! Теперь войдите в систему.")

    def _register_restaurant(self):
        """Регистрация нового ресторана: аккаунт + профиль ресторана."""
        print("\n  --- Регистрация ресторана ---")

        username = input("  Придумайте логин для аккаунта: ").strip()
        if not username:
            print("  [!] Логин не может быть пустым.")
            return
        if self.user_storage.exists(username):
            print("  [!] Пользователь с таким логином уже существует.")
            return

        password = input("  Придумайте пароль: ").strip()
        if not password:
            print("  [!] Пароль не может быть пустым.")
            return

        name = input("  Название ресторана: ").strip()
        if not name:
            print("  [!] Название не может быть пустым.")
            return

        # Выбор типа кухни
        print("\n  Выберите тип кухни:")
        for key, cuisine in CUISINE_TYPES.items():
            print(f"    {key}. {cuisine}")

        cuisine_choice = input("  Ваш выбор: ").strip()
        if cuisine_choice not in CUISINE_TYPES:
            print("  [!] Неверный выбор кухни.")
            return

        cuisine = CUISINE_TYPES[cuisine_choice]

        # Сохраняем пользователя с ролью restaurant
        self.user_storage.save(User(username, password, "restaurant"))
        # Сохраняем профиль ресторана
        self.restaurant_storage.save(Restaurant(username, name, cuisine))

        print(f"\n  [✓] Ресторан «{name}» ({cuisine}) успешно зарегистрирован!")
        print("  Войдите в систему, чтобы добавить блюда в меню.")

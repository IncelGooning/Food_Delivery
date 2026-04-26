import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from cli.auth_menu import AuthMenu
from cli.client_menu import ClientMenu
from cli.courier_menu import CourierMenu
from cli.restaurant_menu import RestaurantMenu

from storage.user_storage import UserStorage
from storage.restaurant_storage import RestaurantStorage
from storage.menu_storage import MenuStorage
from storage.order_storage import OrderStorage


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Создаём все хранилища
    user_storage       = UserStorage(os.path.join(DATA_DIR, "users.txt"))
    restaurant_storage = RestaurantStorage(os.path.join(DATA_DIR, "restaurants.txt"))
    menu_storage       = MenuStorage(os.path.join(DATA_DIR, "menu.txt"))
    order_storage      = OrderStorage(os.path.join(DATA_DIR, "orders.txt"))

    auth_menu = AuthMenu(user_storage, restaurant_storage)

    while True:
        user = auth_menu.show()

        if user is None:
            print("\n  Программа завершена. До свидания!\n")
            break

        if user.role == "client":
            ClientMenu(user, menu_storage, order_storage, restaurant_storage).show()

        elif user.role == "restaurant":
            RestaurantMenu(user, order_storage, menu_storage, restaurant_storage).show()

        elif user.role == "courier":
            CourierMenu(user, order_storage).show()


if __name__ == "__main__":
    main()

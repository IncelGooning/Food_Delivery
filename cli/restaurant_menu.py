# Меню для роли "Ресторан".
# Ресторан может: смотреть свои заказы, менять их статус,
#                 добавлять и удалять блюда в своём меню.

from models.order import Order
from storage.order_storage import OrderStorage
from storage.menu_storage import MenuStorage
from storage.restaurant_storage import RestaurantStorage


class RestaurantMenu:
    def __init__(self, user, order_storage, menu_storage, restaurant_storage):
        self.user = user
        self.order_storage = order_storage
        self.menu_storage = menu_storage
        self.restaurant_storage = restaurant_storage

        # Загружаем профиль этого ресторана
        self.restaurant = restaurant_storage.find_by_username(user.username)

    def show(self):
        name = self.restaurant.name if self.restaurant else self.user.username
        while True:
            print("\n" + "=" * 45)
            print(f"  Ресторан: {name}")
            print("=" * 45)
            print("  1. Мои заказы")
            print("  2. Изменить статус заказа")
            print("  3. Моё меню")
            print("  4. Добавить блюдо в меню")
            print("  5. Удалить блюдо из меню")
            print("  0. Выйти из аккаунта")
            print("-" * 45)

            choice = input("  Ваш выбор: ").strip()

            if choice == "1":
                self._view_my_orders()
            elif choice == "2":
                self._advance_order()
            elif choice == "3":
                self._view_menu()
            elif choice == "4":
                self._add_dish()
            elif choice == "5":
                self._delete_dish()
            elif choice == "0":
                break
            else:
                print("  [!] Неверный пункт. Попробуйте снова.")

    def _view_my_orders(self):
        """Показывает только заказы, сделанные в этот ресторан."""
        print("\n  --- Мои заказы ---")
        # Фильтруем заказы по полю restaurant_username
        my_orders = [o for o in self.order_storage.get_all()
                     if o.restaurant_username == self.user.username]

        if not my_orders:
            print("  Заказов пока нет.")
        else:
            for order in my_orders:
                courier_info = f" | Курьер: {order.courier_username}" if order.courier_username else ""
                print(f"\n  Заказ №{order.order_id} | Клиент: {order.client_username}"
                      f" | Статус: {order.status}{courier_info}")
                for item in order.items:
                    subtotal = item["price"] * item["qty"]
                    print(f"    • {item['name']} × {item['qty']} = {subtotal:.2f} руб.")
                print(f"    Итого: {order.total():.2f} руб.")

        input("\n  Нажмите Enter для продолжения...")

    def _advance_order(self):
        """Продвигает статус заказа на следующий шаг."""
        print("\n  --- Изменение статуса заказа ---")

        advanceable = [o for o in self.order_storage.get_all()
                       if o.restaurant_username == self.user.username
                       and o.status in Order.RESTAURANT_NEXT_STATUS]

        if not advanceable:
            print("  Нет заказов для изменения статуса.")
            input("  Нажмите Enter для продолжения...")
            return

        for order in advanceable:
            next_status = Order.RESTAURANT_NEXT_STATUS[order.status]
            print(f"  Заказ №{order.order_id} | {order.status} → {next_status}"
                  f" | Клиент: {order.client_username}")

        try:
            order_id = int(input("\n  Введите номер заказа: ").strip())
        except ValueError:
            print("  [!] Введите число.")
            input("  Нажмите Enter для продолжения...")
            return

        order = self.order_storage.find_by_id(order_id)

        if not order:
            print("  [!] Заказ не найден.")
        elif order.restaurant_username != self.user.username:
            print("  [!] Это не ваш заказ.")
        elif order.status not in Order.RESTAURANT_NEXT_STATUS:
            print(f"  [!] Невозможно изменить статус «{order.status}».")
        else:
            old_status = order.status
            order.status = Order.RESTAURANT_NEXT_STATUS[old_status]
            self.order_storage.update(order)
            print(f"  [✓] Статус заказа №{order_id}: «{old_status}» → «{order.status}».")

        input("  Нажмите Enter для продолжения...")

    def _view_menu(self):
        """Показывает меню этого ресторана."""
        print("\n  --- Моё меню ---")
        items = self.menu_storage.get_by_restaurant(self.user.username)
        if not items:
            print("  Меню пустое. Добавьте блюда через пункт 4.")
        else:
            for item in items:
                print(f"    {item}")
        input("\n  Нажмите Enter для продолжения...")

    def _add_dish(self):
        """Добавляет новое блюдо в меню ресторана."""
        print("\n  --- Добавить блюдо ---")

        name = input("  Название блюда: ").strip()
        if not name:
            print("  [!] Название не может быть пустым.")
            input("  Нажмите Enter для продолжения...")
            return

        try:
            price = float(input("  Цена (руб.): ").strip())
            if price <= 0:
                raise ValueError
        except ValueError:
            print("  [!] Введите корректную цену (положительное число).")
            input("  Нажмите Enter для продолжения...")
            return

        new_id = self.menu_storage.add_item(self.user.username, name, price)
        print(f"  [✓] Блюдо «{name}» добавлено в меню (ID: {new_id}).")
        input("  Нажмите Enter для продолжения...")

    def _delete_dish(self):
        """Удаляет блюдо из меню ресторана."""
        print("\n  --- Удалить блюдо ---")
        items = self.menu_storage.get_by_restaurant(self.user.username)

        if not items:
            print("  Меню пустое, нечего удалять.")
            input("  Нажмите Enter для продолжения...")
            return

        for item in items:
            print(f"    {item}")

        try:
            item_id = int(input("\n  Введите ID блюда для удаления: ").strip())
        except ValueError:
            print("  [!] Введите число.")
            input("  Нажмите Enter для продолжения...")
            return

        deleted = self.menu_storage.delete_item(item_id, self.user.username)
        if deleted:
            print(f"  [✓] Блюдо удалено из меню.")
        else:
            print("  [!] Блюдо не найдено или не принадлежит вашему ресторану.")
        input("  Нажмите Enter для продолжения...")

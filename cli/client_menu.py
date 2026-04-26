# Меню для роли "Клиент".
# Клиент может: смотреть рестораны (с фильтром по кухне),
#               делать заказ в выбранном ресторане,
#               смотреть свои заказы, отменять заказ.

from models.order import Order
from storage.menu_storage import MenuStorage
from storage.order_storage import OrderStorage
from storage.restaurant_storage import RestaurantStorage
from models.restaurant import CUISINE_TYPES


class ClientMenu:
    def __init__(self, user, menu_storage, order_storage, restaurant_storage):
        self.user = user
        self.menu_storage = menu_storage
        self.order_storage = order_storage
        self.restaurant_storage = restaurant_storage

    def show(self):
        while True:
            print("\n" + "=" * 45)
            print(f"  Меню клиента | {self.user.username}")
            print("=" * 45)
            print("  1. Посмотреть рестораны")
            print("  2. Сделать заказ")
            print("  3. Мои заказы")
            print("  4. Отменить заказ")
            print("  0. Выйти из аккаунта")
            print("-" * 45)

            choice = input("  Ваш выбор: ").strip()

            if choice == "1":
                self._view_restaurants()
            elif choice == "2":
                self._create_order()
            elif choice == "3":
                self._view_my_orders()
            elif choice == "4":
                self._cancel_order()
            elif choice == "0":
                break
            else:
                print("  [!] Неверный пункт. Попробуйте снова.")

    # ------------------------------------------------------------------
    # Просмотр ресторанов с фильтром по кухне
    # ------------------------------------------------------------------

    def _view_restaurants(self):
        """Показывает список ресторанов, опционально фильтруя по кухне."""
        print("\n  --- Рестораны ---")
        print("  Фильтр по кухне (или Enter, чтобы показать все):")
        for key, cuisine in CUISINE_TYPES.items():
            print(f"    {key}. {cuisine}")

        filter_choice = input("  Ваш выбор: ").strip()

        if filter_choice == "":
            restaurants = self.restaurant_storage.get_all()
        elif filter_choice in CUISINE_TYPES:
            cuisine_filter = CUISINE_TYPES[filter_choice]
            restaurants = self.restaurant_storage.find_by_cuisine(cuisine_filter)
        else:
            print("  [!] Неверный выбор. Показываю все рестораны.")
            restaurants = self.restaurant_storage.get_all()

        print()
        if not restaurants:
            print("  Ресторанов не найдено.")
        else:
            for r in restaurants:
                items = self.menu_storage.get_by_restaurant(r.username)
                dish_count = len(items)
                print(f"  • {r.name}  [{r.cuisine}]  |  блюд в меню: {dish_count}")

        input("\n  Нажмите Enter для продолжения...")

    # ------------------------------------------------------------------
    # Создание заказа
    # ------------------------------------------------------------------

    def _create_order(self):
        print("\n  --- Создание заказа ---")

        # Шаг 1: выбор ресторана (с возможным фильтром по кухне)
        restaurant = self._pick_restaurant()
        if not restaurant:
            return

        # Шаг 2: просмотр меню и набор корзины
        items = self.menu_storage.get_by_restaurant(restaurant.username)
        if not items:
            print("  [!] У этого ресторана пока нет блюд в меню.")
            input("  Нажмите Enter для продолжения...")
            return

        print(f"\n  Меню ресторана «{restaurant.name}»:")
        for item in items:
            print(f"    {item}")
        print("-" * 45)
        print("  Вводите ID блюд и количество. Введите 0, чтобы завершить.")

        selected = []  # список словарей: {name, price, qty}

        while True:
            try:
                item_id = int(input("\n  ID блюда (0 — готово): ").strip())
            except ValueError:
                print("  [!] Введите число.")
                continue

            if item_id == 0:
                break

            # Проверяем, что блюдо принадлежит именно этому ресторану
            result = self.menu_storage.find_by_id(item_id)
            if not result:
                print("  [!] Блюда с таким ID не существует.")
                continue

            owner_username, menu_item = result
            if owner_username != restaurant.username:
                print("  [!] Это блюдо не из меню выбранного ресторана.")
                continue

            try:
                qty = int(input(f"  Количество «{menu_item.name}»: ").strip())
            except ValueError:
                print("  [!] Введите целое число.")
                continue

            if qty <= 0:
                print("  [!] Количество должно быть больше нуля.")
                continue

            # Если блюдо уже в корзине — увеличиваем количество
            for s in selected:
                if s["name"] == menu_item.name:
                    s["qty"] += qty
                    print(f"  [+] Обновлено: {menu_item.name} × {s['qty']}")
                    break
            else:
                selected.append({"name": menu_item.name, "price": menu_item.price, "qty": qty})
                print(f"  [+] Добавлено: {menu_item.name} × {qty}")

        if not selected:
            print("  Заказ не создан — корзина пуста.")
            input("  Нажмите Enter для продолжения...")
            return

        # Итог
        print("\n  Ваш заказ:")
        total = 0
        for s in selected:
            subtotal = s["price"] * s["qty"]
            total += subtotal
            print(f"    {s['name']} × {s['qty']} = {subtotal:.2f} руб.")
        print(f"  Итого: {total:.2f} руб.")

        confirm = input("\n  Подтвердить? (да/нет): ").strip().lower()
        if confirm != "да":
            print("  Заказ отменён.")
            input("  Нажмите Enter для продолжения...")
            return

        items_str = ";".join(f"{s['name']}:{s['price']}:{s['qty']}" for s in selected)
        new_id = self.order_storage.next_id()
        order = Order(new_id, self.user.username, restaurant.username, items_str,
                      "Ожидает подтверждения", "")
        self.order_storage.save(order)
        print(f"\n  [✓] Заказ №{new_id} в «{restaurant.name}» создан!")
        print(f"  Статус: «Ожидает подтверждения».")
        input("  Нажмите Enter для продолжения...")

    def _pick_restaurant(self):
        """
        Вспомогательный метод: показывает рестораны с фильтром по кухне
        и возвращает выбранный объект Restaurant или None.
        """
        print("\n  Фильтр по кухне (или Enter, чтобы показать все):")
        for key, cuisine in CUISINE_TYPES.items():
            print(f"    {key}. {cuisine}")

        filter_choice = input("  Ваш выбор: ").strip()

        if filter_choice == "":
            restaurants = self.restaurant_storage.get_all()
        elif filter_choice in CUISINE_TYPES:
            restaurants = self.restaurant_storage.find_by_cuisine(CUISINE_TYPES[filter_choice])
        else:
            print("  [!] Неверный выбор фильтра. Показываю все рестораны.")
            restaurants = self.restaurant_storage.get_all()

        if not restaurants:
            print("  Ресторанов не найдено.")
            input("  Нажмите Enter для продолжения...")
            return None

        print("\n  Доступные рестораны:")
        for i, r in enumerate(restaurants, start=1):
            print(f"    {i}. {r.name}  [{r.cuisine}]")

        try:
            num = int(input("\n  Выберите номер ресторана: ").strip())
            if num < 1 or num > len(restaurants):
                raise ValueError
        except ValueError:
            print("  [!] Неверный выбор.")
            input("  Нажмите Enter для продолжения...")
            return None

        return restaurants[num - 1]

    # ------------------------------------------------------------------
    # Просмотр и отмена заказов
    # ------------------------------------------------------------------

    def _view_my_orders(self):
        print("\n  --- Мои заказы ---")
        my_orders = [o for o in self.order_storage.get_all()
                     if o.client_username == self.user.username]

        if not my_orders:
            print("  У вас пока нет заказов.")
        else:
            for order in my_orders:
                # Получаем название ресторана для красивого отображения
                rest = self.restaurant_storage.find_by_username(order.restaurant_username)
                rest_name = rest.name if rest else order.restaurant_username
                print(f"\n  Заказ №{order.order_id} | {rest_name} | Статус: {order.status}")
                for item in order.items:
                    subtotal = item["price"] * item["qty"]
                    print(f"    • {item['name']} × {item['qty']} = {subtotal:.2f} руб.")
                print(f"    Итого: {order.total():.2f} руб.")

        input("\n  Нажмите Enter для продолжения...")

    def _cancel_order(self):
        print("\n  --- Отмена заказа ---")
        cancellable = [o for o in self.order_storage.get_all()
                       if o.client_username == self.user.username and o.can_be_cancelled()]

        if not cancellable:
            print("  Нет заказов, которые можно отменить.")
            input("  Нажмите Enter для продолжения...")
            return

        for order in cancellable:
            print(f"  Заказ №{order.order_id} | {order.status} | {order.total():.2f} руб.")

        try:
            order_id = int(input("\n  Введите номер заказа для отмены: ").strip())
        except ValueError:
            print("  [!] Введите число.")
            input("  Нажмите Enter для продолжения...")
            return

        order = self.order_storage.find_by_id(order_id)

        if not order:
            print("  [!] Заказ не найден.")
        elif order.client_username != self.user.username:
            print("  [!] Это не ваш заказ.")
        elif not order.can_be_cancelled():
            print(f"  [!] Заказ со статусом «{order.status}» нельзя отменить.")
        else:
            order.status = "Отменён"
            self.order_storage.update(order)
            print(f"  [✓] Заказ №{order_id} отменён.")

        input("  Нажмите Enter для продолжения...")

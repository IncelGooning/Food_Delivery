# Меню для роли "Курьер".
# Курьер может: смотреть готовые заказы, взять заказ, завершить доставку,
#               смотреть свои доставленные заказы.

from storage.order_storage import OrderStorage


class CourierMenu:
    def __init__(self, user, order_storage):
        self.user = user
        self.order_storage = order_storage

    def show(self):
        while True:
            print("\n" + "=" * 45)
            print(f"  Меню курьера | {self.user.username}")
            print("=" * 45)
            print("  1. Заказы, готовые к выдаче")
            print("  2. Взять заказ в доставку")
            print("  3. Завершить доставку")
            print("  4. Мои доставленные заказы")
            print("  0. Выйти из аккаунта")
            print("-" * 45)

            choice = input("  Ваш выбор: ").strip()

            if choice == "1":
                self._view_ready_orders()
            elif choice == "2":
                self._take_order()
            elif choice == "3":
                self._complete_delivery()
            elif choice == "4":
                self._view_delivered_orders()
            elif choice == "0":
                break
            else:
                print("  [!] Неверный пункт. Попробуйте снова.")

    def _view_ready_orders(self):
        print("\n  --- Заказы, готовые к выдаче ---")
        ready = [o for o in self.order_storage.get_all()
                 if o.status == "Готов к выдаче"]

        if not ready:
            print("  Нет заказов, ожидающих курьера.")
        else:
            for order in ready:
                print(f"  Заказ №{order.order_id} | Клиент: {order.client_username}"
                      f" | Сумма: {order.total():.2f} руб.")

        input("\n  Нажмите Enter для продолжения...")

    def _take_order(self):
        print("\n  --- Взять заказ в доставку ---")
        ready = [o for o in self.order_storage.get_all()
                 if o.status == "Готов к выдаче"]

        if not ready:
            print("  Нет заказов для принятия.")
            input("  Нажмите Enter для продолжения...")
            return

        for order in ready:
            print(f"  Заказ №{order.order_id} | {order.total():.2f} руб."
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
        elif order.status != "Готов к выдаче":
            print("  [!] Этот заказ недоступен для принятия.")
        else:
            order.status = "В пути"
            order.courier_username = self.user.username
            self.order_storage.update(order)
            print(f"  [✓] Вы взяли заказ №{order_id}. Удачной доставки!")

        input("  Нажмите Enter для продолжения...")

    def _complete_delivery(self):
        print("\n  --- Завершить доставку ---")
        # Ищем заказы, которые везёт именно этот курьер
        my_active = [o for o in self.order_storage.get_all()
                     if o.courier_username == self.user.username and o.status == "В пути"]

        if not my_active:
            print("  У вас нет активных доставок.")
            input("  Нажмите Enter для продолжения...")
            return

        for order in my_active:
            print(f"  Заказ №{order.order_id} | {order.total():.2f} руб."
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
        elif order.courier_username != self.user.username:
            print("  [!] Это не ваш заказ.")
        elif order.status != "В пути":
            print("  [!] Этот заказ не в доставке.")
        else:
            order.status = "Доставлен"
            self.order_storage.update(order)
            print(f"  [✓] Заказ №{order_id} доставлен клиенту!")

        input("  Нажмите Enter для продолжения...")

    def _view_delivered_orders(self):
        print("\n  --- Мои доставленные заказы ---")
        delivered = [o for o in self.order_storage.get_all()
                     if o.courier_username == self.user.username and o.status == "Доставлен"]

        if not delivered:
            print("  Доставленных заказов пока нет.")
        else:
            for order in delivered:
                print(f"  Заказ №{order.order_id} | Клиент: {order.client_username}"
                      f" | Сумма: {order.total():.2f} руб.")

        input("\n  Нажмите Enter для продолжения...")

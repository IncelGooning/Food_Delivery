import os
from models.order import Order


class OrderStorage:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            open(filepath, "w", encoding="utf-8").close()

    def _read_all(self):
        orders = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                orders.append(Order(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]))
        return orders

    def _write_all(self, orders):
        with open(self.filepath, "w", encoding="utf-8") as f:
            for order in orders:
                f.write(
                    f"{order.order_id}|"
                    f"{order.client_username}|"
                    f"{order.restaurant_username}|"
                    f"{order.items_to_str()}|"
                    f"{order.status}|"
                    f"{order.courier_username}\n"
                )

    def get_all(self):
        return self._read_all()

    def find_by_id(self, order_id):
        for order in self._read_all():
            if order.order_id == int(order_id):
                return order
        return None

    def save(self, order):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(
                f"{order.order_id}|"
                f"{order.client_username}|"
                f"{order.restaurant_username}|"
                f"{order.items_to_str()}|"
                f"{order.status}|"
                f"{order.courier_username}\n"
            )

    def update(self, updated_order):
        orders = self._read_all()
        for i, order in enumerate(orders):
            if order.order_id == updated_order.order_id:
                orders[i] = updated_order
                break
        self._write_all(orders)

    def next_id(self):
        orders = self._read_all()
        if not orders:
            return 1
        return max(order.order_id for order in orders) + 1

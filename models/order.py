# Модель заказа.
# Статусы заказа:
#   Ожидает подтверждения -> Готовится -> Готов к выдаче -> В пути -> Доставлен (отменен)

class Order:
    RESTAURANT_NEXT_STATUS = {
        "Ожидает подтверждения": "Готовится",
        "Готовится": "Готов к выдаче",
    }

    def __init__(self, order_id, client_username, restaurant_username, items_str, status, courier_username):
        self.order_id = int(order_id)
        self.client_username = client_username
        self.restaurant_username = restaurant_username  # к какому ресторану относится заказ

        self.items = self._parse_items(items_str)

        self.status = status
        self.courier_username = courier_username  

    def _parse_items(self, items_str):
        """Превращает строку с блюдами в список словарей."""
        items = []
        if not items_str:
            return items
        for part in items_str.split(";"):
            name, price, qty = part.split(":")
            items.append({
                "name": name,
                "price": float(price),
                "qty": int(qty),
            })
        return items

    def items_to_str(self):
        """Превращает список блюд обратно в строку для записи в файл."""
        parts = []
        for item in self.items:
            parts.append(f"{item['name']}:{item['price']}:{item['qty']}")
        return ";".join(parts)

    def total(self):
        """Считает итоговую сумму заказа."""
        return sum(item["price"] * item["qty"] for item in self.items)

    def can_be_cancelled(self):
        """Можно ли отменить заказ."""
        return self.status in ("Ожидает подтверждения", "Готовится")

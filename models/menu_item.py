# Модель одной позиции 
class MenuItem:
    def __init__(self, item_id, name, price):
        self.item_id = int(item_id)  # уникальный номер блюда
        self.name = name             # название
        self.price = float(price)   # цена в рублях

    def __str__(self):
        return f"[{self.item_id}] {self.name} — {self.price:.2f} руб."

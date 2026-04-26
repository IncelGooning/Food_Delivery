
# Доступные типы кухни
CUISINE_TYPES = {
    "1": "Итальянская",
    "2": "Японская",
    "3": "Азиатская",
    "4": "Фастфуд",
    "5": "Европейская",
    "6": "Грузинская",
    "7": "Русская",
}

class Restaurant:
    def __init__(self, username, name, cuisine):
        self.username = username  # логин владельца ресторана
        self.name = name          # название ресторана
        self.cuisine = cuisine    # тип кухни 

    def __str__(self):
        return f"{self.name} ({self.cuisine})"

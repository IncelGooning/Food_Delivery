import os
from models.restaurant import Restaurant


class RestaurantStorage:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            open(filepath, "w", encoding="utf-8").close()

    def _read_all(self):
        restaurants = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                restaurants.append(Restaurant(parts[0], parts[1], parts[2]))
        return restaurants

    def _write_all(self, restaurants):
        with open(self.filepath, "w", encoding="utf-8") as f:
            for r in restaurants:
                f.write(f"{r.username}|{r.name}|{r.cuisine}\n")

    def get_all(self):
        return self._read_all()

    def find_by_username(self, username):
        for r in self._read_all():
            if r.username == username:
                return r
        return None

    def find_by_cuisine(self, cuisine):
        return [r for r in self._read_all() if r.cuisine == cuisine]

    def save(self, restaurant):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"{restaurant.username}|{restaurant.name}|{restaurant.cuisine}\n")

    def exists_by_username(self, username):
        return self.find_by_username(username) is not None

import os
from models.menu_item import MenuItem


class MenuStorage:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            open(filepath, "w", encoding="utf-8").close()

    def _read_all(self):
        result = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                item = MenuItem(parts[0], parts[2], parts[3])
                result.append((parts[1], item))  # (restaurant_username, MenuItem)
        return result

    def get_all(self):
        return self._read_all()

    def get_by_restaurant(self, restaurant_username):
        return [item for owner, item in self._read_all()
                if owner == restaurant_username]

    def find_by_id(self, item_id):
        for owner, item in self._read_all():
            if item.item_id == int(item_id):
                return owner, item
        return None

    def add_item(self, restaurant_username, name, price):
        new_id = self._next_id()
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"{new_id}|{restaurant_username}|{name}|{price}\n")
        return new_id

    def delete_item(self, item_id, restaurant_username):
        all_items = self._read_all()
        new_items = []
        deleted = False
        for owner, item in all_items:
            if item.item_id == int(item_id) and owner == restaurant_username:
                deleted = True  # пропускаем — удаляем
            else:
                new_items.append((owner, item))

        if deleted:
            with open(self.filepath, "w", encoding="utf-8") as f:
                for owner, item in new_items:
                    f.write(f"{item.item_id}|{owner}|{item.name}|{item.price}\n")
        return deleted

    def _next_id(self):
        all_items = self._read_all()
        if not all_items:
            return 1
        return max(item.item_id for _, item in all_items) + 1

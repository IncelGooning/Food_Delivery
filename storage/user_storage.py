import os
from models.user import User


class UserStorage:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            open(filepath, "w", encoding="utf-8").close()

    def _read_all(self):
        users = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                users.append(User(parts[0], parts[1], parts[2]))
        return users

    def _write_all(self, users):
        with open(self.filepath, "w", encoding="utf-8") as f:
            for user in users:
                f.write(f"{user.username}|{user.password}|{user.role}\n")

    def find_by_username(self, username):
        for user in self._read_all():
            if user.username == username:
                return user
        return None

    def save(self, user):
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"{user.username}|{user.password}|{user.role}\n")

    def exists(self, username):
        return self.find_by_username(username) is not None

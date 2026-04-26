# Роли: client (клиент), courier (курьер), restaurant (ресторан).

class User:
    def __init__(self, username, password, role):
        self.username = username  # логин
        self.password = password  # пароль
        self.role = role          # роль

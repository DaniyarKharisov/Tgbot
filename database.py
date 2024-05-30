import sqlite3

class User:
    def __init__(self, user_id: int, city: str | None = None):
        self.user_id = user_id
        self.city = city
    def __init__(self, user_id: int, city: str | None = None):
        self.user_id = user_id
        self.city = city

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("sqlite.db")
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def get_user(self, user_id: int) -> User | None:
        query = "SELECT * FROM users WHERE id = ?"              # запрос
        args = (user_id,)                                       # аргументы
        self.cursor.execute(query, args)                        # выполняем запрос
        row = self.cursor.fetchone()                            # получаем кортеж с пользователем
        if row is None:                                         # проверяем, вернулось ли нам что-либо
            return None                                         # если ничего не вернулось, возвращаем None
        return User(user_id=user_id, city=row[1])               # если данные получены, возвращаем пользователя

    def create_user(self, user_id: int):
        query = "INSERT INTO users(id) VALUES (?)"              # запрос
        args = (user_id,)                                       # аргументы
        self.cursor.execute(query, args)                        # выполняем запрос
        self.connection.commit()                                # сохраняем изменения

    def set_city(self, user_id: int, city: str):
        query = "UPDATE users SET city = ? WHERE id = ?"        # запрос

        args = (city, user_id)                                  # аргументы
        self.cursor.execute(query, args)                        # выполняем запрос
        self.connection.commit()                                # сохраняем изменения
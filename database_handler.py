import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.db_name = "GaseNotes.db"
        self.database = sqlite3.connect(self.db_name)
        self.cursor = self.database.cursor()
        self.database_users_initialize()


    def database_users_initialize(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            username TEXT NOT NULL PRIMARY KEY,
            language TEXT NOT NULL
            )
            ''')
        self.database.commit()

    def insert(self, val: list, col: list, table: str):
        if not val or not col:
            raise ValueError("Values and columns cannot be empty")
        placeholders = ", ".join(["?"] * len(val))
        query = f'INSERT INTO {table} ({", ".join(col)}) VALUES ({placeholders})'
        self.cursor.execute(query, val)
        self.database.commit()

    def find_user(self, name):
        self.cursor.execute(f'SELECT * FROM Users WHERE username = "{name}"')
        return self.cursor.fetchall()

    def determine_lang(self, name):
        user_data = self.find_user(name)
        if user_data:
            return user_data[0][1]  # Возвращаем язык из первого найденного пользователя
        else:
            return "english"

    def hint_category_to_user_add(self, username: str, category_and_hints: dict, is_date_on):
        if not category_and_hints:
            raise ValueError("Category and hints cannot be empty")

        # Проверяем, что имена категорий безопасны для SQL
        for category in category_and_hints.keys():
            if not category.replace("_", "").isalnum():
                raise ValueError(f"Invalid category name: {category}")

        self.cursor.execute(f"SELECT * FROM Users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user is None:
            raise ValueError("User not found")

        # Создаем таблицу с динамическими колонками
        columns = [f"{category} TEXT NOT NULL" for category in category_and_hints.keys()]
        columns.append("hint TEXT NOT NULL")
        if is_date_on:
            columns.append("date TEXT NOT NULL")

        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {username}_notes (
            {", ".join(columns)}
        )
        '''
        self.cursor.execute(create_table_query)
        self.database.commit()

        # Вставляем подсказки
        for category, hints in category_and_hints.items():
            if isinstance(hints, list):
                hints_str = ", ".join(hints)
                self.insert(val=[f"{category}:{hints_str}"], col=["hint"], table=f"{username}_notes")
            else:
                raise ValueError("Hints must be a list")

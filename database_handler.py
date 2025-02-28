import sqlite3


class DatabaseHandler:
    def __init__(self):
        self.db_name = 'GaseNotes.db'
        self.__table_users_creation()
        self.__table_categories_creation()
        self.__table_hints_creation()

    def __table_users_creation(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,  
        language TEXT NOT NULL
        )
        ''')
        connection.commit()
        connection.close()

    def __table_categories_creation(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
        category_owner_id INTEGER,
        categories TEXT NOT NULL,
        FOREIGN KEY (category_owner_id) REFERENCES Users (user_id)
        )
        ''')
        connection.commit()
        connection.close()

    def __table_hints_creation(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Hints (
        category TEXT NOT NULL,
        hints TEXT NOT NULL,
        FOREIGN KEY (category) REFERENCES Categories (categories)
        )
        ''')
        connection.commit()
        connection.close()

    def add_user(self, user, lang):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (username, language) VALUES (?, ?)", (user, lang))
        connection.commit()
        connection.close()

    def update_users_language(self, username, language):
        username, language = username.lower(), language.lower()
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE Users SET language = ? WHERE username = ?", (language, username))
        connection.commit()
        connection.close()

    def determine_lang(self, username):
        username = username.lower()
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT language FROM Users WHERE username = ?", (username, ))
        res = cursor.fetchone()
        connection.close()
        return res

    def get_id_from_user(self, user_name):
        user_name = user_name.lower()
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE category_owner_id = ?", (user_name,))
        res = cursor.fetchone()
        connection.close()
        if res is None:
            raise ValueError("User does not exist")
        else:
            return res[0]

    def add_category(self, user_name, category):
        user_name, category = user_name.lower(), category.lower()
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Categories (category_owner_id, categories) VALUES (?, ?)",
                       (self.get_id_from_user(user_name), category))
        connection.commit()
        connection.close()

    def add_hints_and_category(self, username, category, hints):
        username, category = username.lower(), category.lower()
        hints[::].lower()
        self.add_category(username, category)
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Hints (category, hints) VALUES (?, ?)", (category, hints))
        connection.commit()
        connection.close()

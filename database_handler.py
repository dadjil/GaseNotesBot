import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.connection = sqlite3.connect('GaseNotes.db')
        self.cursor = self.connection.cursor()
        self.__table_users_creation()
        self.__table_categories_creation()
        self.__table_hints_creation()

    def __table_users_creation(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        username TEXT NOT NULL PRIMARY KEY,
        language TEXT NOT NULL
        )
        ''')
        self.connection.commit()

    def __table_categories_creation(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
        category_owner TEXT NOT NULL,
        categories TEXT NOT NULL,
        FOREIGN KEY (category_owner) REFERENCES Users (username)
        )
        ''')
        self.connection.commit()

    def __table_hints_creation(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Hints (
        FOREIGN KEY (category) REFERENCES Categories (categories),
        hints TEXT NOT NULL
        )
        ''')
        self.connection.commit()
   def add_user(self, username, language):
       self.cursor.execute("INSERT INTO Users (username, language) VALUES (?, ?)", (username, language))
       self.connection.commit()
   def update_users_language(self, username, language):
       self.cursor.execute("UPDATE Users SET language = ? WHERE username = ?", (language, username))
       self.connection.commit()

    def determine_lang(self, username):
        self.cursor.execute("SELECT language FROM Users WHERE username = ?", (username,))
        return self.cursor.fetchone()[0]



    def __del__(self):
        self.connection.close()

import sqlite3

class DatabaseHandler:
    def __init__(self):
        self.db_name = "GaseNotes.db"
        self.database = sqlite3.connect(self.db_name)
        self.database_users_initialize()
        self.cursor = self.database.cursor()

    def database_users_initialize(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            username TEXT NOT NULL PRIMARY KEY,
            date_on INT,
            num_on INT,
            language TEXT NOT NULL
            )
            ''')
        self.database.commit()

    def insert(self, val, col, table):
        if isinstance(val, str):
            self.cursor.execute(f'INSERT INTO {table} VALUES ({val}, "{col}")')
        elif isinstance(val, list):
            if isinstance(col, str):
                self.cursor.execute(f"INSERT INTO {table} ({col}) VALUES ({', '.join(['?'] * len(val))})", val)
            elif isinstance(col, list):
                self.cursor.execute(f"INSERT INTO {table} {', '.join(col)} VALUES ({', '.join(['?'] * len(val))})", val)
        else:
            raise AttributeError
        self.database.commit()



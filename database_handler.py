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
        self.cursor.execute(f'INSERT INTO {table} ({", ".join(col)}) VALUES ({", ".join(val)})')
        self.database.commit()

    def find_user(self, name):
        self.cursor.execute(f'SELECT * FROM Users WHERE username = "{name}"')
        return self.cursor.fetchall()

    def determine_lang(self, name):
        return self.find_user(name)[1]

    def hint_category_to_user_add(self, username: str, category_and_hints: dict, is_date_on):
        # category_and_hints is like str(category): list(hints)
        self.cursor.execute(f"SELECT * FROM Users WHERE username = '{username}'")
        user = self.cursor.fetchone()
        if user is None:
            raise ValueError
        else:
            categories = [str(key)+" TEXT NOT NULL," for key in category_and_hints.keys()]
            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {user[0]+"_notes"}(
            {"\n".join(categories)}
            hint TEXT NOT NULL,
            {"date TEXT NOT NULL," if is_date_on else ""}
            )
            ''')
            self.database.commit()

            for key, value in category_and_hints.items():
                if isinstance(value, list):
                    self.insert(val=str(key)+":"+",".join(str(value)), col="hint", table=f"{user[0]}_notes")
                else:
                    raise ValueError

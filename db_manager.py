import mysql.connector

class DBManager:
    def __init__(self, user, password, database, table) -> None:
        self.user = user
        self.password = password
        self.database = database
        self.table = table

        self.connect_to_db()
        self.create_cursor()
    

    def connect_to_db(self) -> None:
        self.db = mysql.connector.connect(
            host="localhost",
            user=self.user,
            password=self.password,
            database=self.database
        )


    def create_cursor(self) -> None:
        self.cursor = self.db.cursor()


    def insert_into_db(self, name: str, company: str, address: str, pay: int) -> None:
        sql = f"INSERT INTO {self.table} (title, employer, address, pay) VALUES (%s, %s, %s, %s)"
        values = (name, company, address, pay)
        self.cursor.execute(sql, values)
        self.db.commit()

import mysql.connector
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="PythonDB",
                user="root",  # יש להחליף לשם המשתמש שלך
                password="123321",  # יש להחליף לסיסמה שלך
                database="mypythonschem"  # יש להחליף לשם בסיס הנתונים
            )
            return True
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            return False

    def save_game_result(self, nickname, score):
        if not self.connection:
            if not self.connect():
                return False

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO users (nickname, game_date, score) VALUES (%s, %s, %s)"
            current_time = datetime.now()
            cursor.execute(query, (nickname, current_time, score))
            self.connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Error saving game result: {err}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
import pygame
import mysql.connector
from datetime import datetime


class GameOverView:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load("images/gameOver.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.font = pygame.font.Font('./fonts/GROBOLD.ttf', 48)
        self.restart_font = pygame.font.Font('./fonts/GROBOLD.ttf', 36)
        self.db_connection = None
        self.data_saved = False
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123321",
                database="mypythonschem"
            )
        except mysql.connector.Error as err:
            print(f"שגיאה בחיבור לבסיס הנתונים: {err}")

    def save_game_data(self, nickname, score):
        if not self.db_connection:
            return False

        try:
            cursor = self.db_connection.cursor()
            query = "INSERT INTO users (nickname, game_date, score) VALUES (%s, %s, %s)"
            current_time = datetime.now()
            cursor.execute(query, (nickname, current_time, score))
            self.db_connection.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"שגיאה בשמירת נתונים: {err}")
            return False

    def draw(self, screen, score, player_name):
        screen.blit(self.background, (0, 0))

        # שמירת הנתונים אם עדיין לא נשמרו
        if not self.data_saved:
            if self.save_game_data(player_name, score):
                self.data_saved = True
            else:
                error_text = self.restart_font.render("Failed to save results", True, (255, 0, 0))
                screen.blit(error_text,
                            (self.screen_width // 2 - error_text.get_width() // 2, self.screen_height // 2 + 150))

        # הצגת פרטי המשחק
        score_text = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        name_text = self.font.render(f"Player: {player_name}", True, (255, 255, 255))
        restart_text = self.restart_font.render("Press SPACE to restart or ESC to exit", True, (255, 255, 255))

        screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, self.screen_height // 2 - 200))
        screen.blit(name_text, (self.screen_width // 2 - name_text.get_width() // 2, self.screen_height // 2 - 150))
        screen.blit(restart_text,
                    (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height // 2 + 100))

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()
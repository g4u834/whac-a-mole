import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# הגדרות חיבור לבסיס הנתונים
config = {
    'user': 'root',
    'password': '123321',
    'host': 'localhost',
    'database': 'mypythonschem',
    'raise_on_warnings': True
}


def get_data_from_db():
    try:
        # יצירת חיבור
        connection = mysql.connector.connect(**config)

        # שאילתה לשליפת כל הנתונים
        query = """
        SELECT user_id, nickname, game_date, score 
        FROM users
        ORDER BY game_date
        """

        # קריאה לבסיס הנתונים והמרה ל-DataFrame
        df = pd.read_sql(query, connection)

        # הוספת עמודות לניתוח
        df['game_date'] = pd.to_datetime(df['game_date'])
        df['hour'] = df['game_date'].dt.hour
        df['day_part'] = df['hour'].apply(lambda x: 'יום' if 6 <= x < 18 else 'לילה')
        df['day_of_week'] = df['game_date'].dt.day_name()

        return df

    except mysql.connector.Error as err:
        print(f"שגיאה: {err}")
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def day_night_analysis(df):
    # חישוב ממוצעים
    day_night_avg = df.groupby('day_part')['score'].mean()

    # גרף עמודות
    plt.figure(figsize=(10, 6))
    day_night_avg.plot(kind='bar', color=['gold', 'navy'])
    plt.title('השוואת ממוצע ניקוד בשעות היום והלילה')
    plt.ylabel('ניקוד ממוצע')
    plt.xlabel('חלק מהיממה')
    plt.xticks(rotation=0)
    plt.show()

    # גרף חום לפי שעות
    pivot_hour = df.pivot_table(index='hour', values='score', aggfunc='mean')

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_hour, cmap='YlOrRd', annot=True, fmt=".0f")
    plt.title('חום ניקוד ממוצע לפי שעה ביממה')
    plt.show()


def compare_players(df, player1, player2):
    players_df = df[df['nickname'].isin([player1, player2])]

    # השוואת ניקוד ממוצע
    avg_scores = players_df.groupby('nickname')['score'].mean()

    plt.figure(figsize=(10, 6))
    avg_scores.plot(kind='bar', color=['skyblue', 'lightgreen'])
    plt.title(f'השוואת ניקוד ממוצע בין {player1} ל-{player2}')
    plt.ylabel('ניקוד ממוצע')
    plt.show()

    # השוואה לאורך זמן
    pivot_players = players_df.pivot_table(index='game_date', columns='nickname', values='score')

    plt.figure(figsize=(12, 6))
    pivot_players.plot(marker='o')
    plt.title(f'התפתחות ניקוד לאורך זמן')
    plt.ylabel('ניקוד')
    plt.grid(True)
    plt.show()


def player_hours_analysis(df, player_name):
    player_df = df[df['nickname'] == player_name]

    # פילוג שעות משחק
    hour_dist = player_df['hour'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    hour_dist.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title(f'פילוג שעות משחק עבור {player_name}')
    plt.ylabel('')
    plt.show()

    # ניקוד ממוצע לפי שעה
    hour_avg = player_df.groupby('hour')['score'].mean()

    plt.figure(figsize=(12, 6))
    hour_avg.plot(kind='bar', color='purple')
    plt.title(f'ניקוד ממוצע לפי שעה עבור {player_name}')
    plt.xlabel('שעה ביממה')
    plt.ylabel('ניקוד ממוצע')
    plt.xticks(rotation=0)
    plt.show()


def player_time_analysis(df, player_name):
    player_df = df[df['nickname'] == player_name].sort_values('game_date')

    # ניתוח מגמת ניקוד
    plt.figure(figsize=(14, 7))
    plt.plot(player_df['game_date'], player_df['score'], marker='o', linestyle='-', color='teal')

    # הוספת קו מגמה
    x = pd.to_numeric(player_df['game_date']).values.reshape(-1, 1)
    y = player_df['score'].values

    from sklearn.linear_model import LinearRegression
    model = LinearRegression().fit(x, y)
    trend = model.predict(x)

    plt.plot(player_df['game_date'], trend, color='red', linestyle='--',
             label=f'מגמה (שיפוע: {model.coef_[0]:.2f})')

    plt.title(f'התפתחות ניקוד לאורך זמן עבור {player_name}')
    plt.xlabel('תאריך')
    plt.ylabel('ניקוד')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

    # ניתוח לפי יום בשבוע
    day_avg = player_df.groupby('day_of_week')['score'].mean().reindex([
        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
    ])

    plt.figure(figsize=(10, 6))
    day_avg.plot(kind='bar', color='orange')
    plt.title(f'ניקוד ממוצע לפי יום בשבוע עבור {player_name}')
    plt.xlabel('יום בשבוע')
    plt.ylabel('ניקוד ממוצע')
    plt.show()


# שליפת הנתונים
game_data = get_data_from_db()
if game_data is None:
    exit()
#A
#day_night_analysis(game_data)
#B
#compare_players(game_data, 'Tom', 'Sam')
#C
#player_hours_analysis(game_data, 'Eva')
#D
player_time_analysis(game_data, 'Ted')

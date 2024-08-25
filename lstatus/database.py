import sqlite3

class DatabaseHandler:
    def __init__(self, database='logs.db'):
        self.database = database
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS logs
                              (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                              event TEXT NOT NULL, 
                              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            conn.commit()

    def get_logs(self, limit=5):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?', (limit,))
            return cursor.fetchall()

    def get_last_event(self):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT event FROM logs ORDER BY timestamp DESC LIMIT 1')
            event = cursor.fetchone()
            return event[0] if event else None

    def log_event(self, event):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (event) VALUES (?)", (event,))
            conn.commit()

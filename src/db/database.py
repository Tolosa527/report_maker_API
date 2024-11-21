from sqlite3 import connect
from datetime import datetime
from src.logger import Logger
from src.settings import settings
from src.clients.parser.tasks_parser import Task
from typing import Optional

log = Logger().get_logger(__name__)


class Database:

    def __init__(self, test_db=None):
        db_name = test_db if test_db else settings.database_name
        self.conn = connect(db_name)
        self.cursor = self.conn.cursor()

    def add_message(self, text: str, date: Optional[str] = None):
        current_date = date if date else datetime.now()
        self.cursor.execute(
            'INSERT INTO messages (text, date) VALUES (?, ?)',
            (text, current_date)
        )
        self.conn.commit()
        log.info('Added message to database')

    def get_messages(self, start_date=None, end_date=None) -> list[tuple]:
        if not start_date or not end_date:
            tasks = self.cursor.execute('SELECT * FROM messages')
        else:
            tasks = self.cursor.execute(
                'SELECT * FROM messages WHERE date BETWEEN ? AND ?',
                (start_date, end_date)
            )
        return tasks.fetchall()

    def initialize(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS messages '
            '(id INTEGER PRIMARY KEY, text TEXT, date TEXT)'
        )
        self.conn.commit()
        log.info('Initialized message table')

    def bulk_insert(self, messages: list[Task]):
        for message in messages:
            self.add_message(message.title, message.date)


if __name__ == "__main__":
    db = Database().initialize()

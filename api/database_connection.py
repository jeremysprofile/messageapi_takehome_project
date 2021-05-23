import mariadb
import logging
from .database_calls import CREATE_PARTNERS_TABLE, CREATE_MESSAGES_TABLE, GET_PARTNER_ID, WRITE_MESSAGE

from typing import List


class DatabaseConnection:
    CONFIG = {
        'host': 'message-db',
        'port': 3306,
        'user': 'root',
        'password': 'guild',
        'database': 'messageapi'
    }

    def __init__(self,):
        self.conn = None
        self.create_db_connection()
        assert self.conn is not None  # PyCharm type hinting
        self.cursor = self.conn.cursor()

    def __enter__(self,):
        self.create_cursor()
        return self

    def create_cursor(self):
        if self.cursor is None:
            self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None

    def create_db_connection(self, ):
        if self.conn is None:
            self.conn = mariadb.connect(**self.CONFIG)

    def db_setup(self):
        table_creation = [
            CREATE_PARTNERS_TABLE,
            CREATE_MESSAGES_TABLE
        ]
        logging.info("creating DB schema")
        for table_create in table_creation:
            self.cursor.execute(table_create)

    def get_partner_id(self, user1: str, user2: str) -> int:
        """Return the ID of this user-user relationship.
        Creates if nonexistent."""
        # enforce unique partner relationship by just always shoving the lexicographically first username
        # in the first slot
        if user1 < user2:
            pass
        else:
            user1, user2 = user2, user1
        self.cursor.execute(GET_PARTNER_ID, (user1, user2, user1, user2))
        # should be unique, so only one row in
        rows = self.cursor.fetchall()
        assert len(rows) == 1, f"Got more rows than expected from partner query! Received {rows=}"
        return rows[0][0]

    def write_message(self, partner_id: int, sender: str, message: str):
        """Write a message to the DB"""
        self.cursor.execute(WRITE_MESSAGE, partner_id, sender, message)

    def get_messages(self, partner_id: int, count=None, timestamp=None) -> List[str]:
        pass
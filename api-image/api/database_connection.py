import mariadb
import logging
from .database_calls import WRITE_PARTNERS, GET_PARTNER_ID, WRITE_MESSAGE

from typing import List


class DatabasePool:
    def __init__(self):
        self.pool = mariadb.ConnectionPool(
            pool_name='pool',
            pool_size=3,
            pool_reset_connection=False,
            host='message-db',
            port=3306,
            user='root',
            password='guild',
            database='messageapi',
        )

    def get_connection(self):
        return self.pool.get_connection()


class DatabaseConnection:
    def __init__(self, pool):
        self.conn = None
        self.create_db_connection(pool)
        assert self.conn is not None  # PyCharm type hinting
        self.cursor = self.conn.cursor()

    def create_db_connection(self, pool):
        if self.conn is None:
            self.conn = pool.get_connection()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def _get_partner_id(self, user1: str, user2: str) -> int:
        """Return the ID of this user-user relationship.
        Creates if nonexistent."""
        # enforce unique partner relationship by just always shoving the lexicographically first username
        # in the first slot
        if user1 < user2:
            pass
        else:
            user1, user2 = user2, user1
        self.cursor.execute(WRITE_PARTNERS, (user1, user2))
        self.cursor.execute(GET_PARTNER_ID, (user1, user2))
        # should be unique, so only one row in
        rows = self.cursor.fetchall()
        logging.info(f"Response from getting partner id: {rows=}")
        assert len(rows) == 1, f"Got more rows than expected from partner query! Received {rows=}"
        return rows[0][0]

    def write_message(self, sender: str, recipient: str, message: str):
        """Write a message to the DB"""
        partner_id = self._get_partner_id(sender, recipient)
        self.cursor.execute(WRITE_MESSAGE, (partner_id, sender, message))
        # Spent 2 hours realizing I needed this >.<
        self.conn.commit()

    def get_messages(self, partner_id: int, count=None, timestamp=None) -> List[str]:
        pass
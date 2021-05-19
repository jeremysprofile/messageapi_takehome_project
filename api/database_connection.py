import mariadb
import logging


class DatabaseConnection:
    CONFIG = {
        'host': 'message-db',
        'port': 3306,
        'user': 'root',
        'password': 'guild',
        'database': 'messageapi'
    }

    def __init__(self,):
        self.cursor = self.create_db_connection()

    def __enter__(self,):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_db_connection(self, ):
        """Creates the database connection and the database and tables we want.
        Returns the cursor"""
        conn = mariadb.connect(**self.CONFIG)
        cursor = conn.cursor()
        return cursor

    def db_setup(self):
        table_creation = [
            """
            CREATE TABLE usernames (
              id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              username CHAR(15) NOT NULL
            );
            """,
            """
            CREATE TABLE partners (
            partner_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            user_id_1 INT NOT NULL,
            user_id_2 INT NOT NULL,
            FOREIGN KEY (user_id_1)
              REFERENCES usernames(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id_2)
              REFERENCES usernames(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE messages (
            id INT NOT NULL auto_increment primary key,
            sent timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            sender INT NOT NULL,
            FOREIGN KEY (sender)
              REFERENCES usernames(id) ON DELETE CASCADE
            );
            """,
        ]
        logging.info("creating DB schema")
        for table_create in table_creation:
            self.cursor.execute(table_create)

    def close(self,):
        if self.cursor is not None:
            self.cursor.close()
        self.cursor = None

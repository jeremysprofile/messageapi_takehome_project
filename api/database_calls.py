import mariadb
import logging

# the partners schema does not enforce user1 < user2
# so if you use it wrong, you could have an id, user1, user2 and an id, user2, user1 row
# I can't tell if partners creates an index on the users, but I *think* it does?
CREATE_PARTNERS_TABLE = """
    CREATE TABLE partners (
        relationship_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_1 TINYTEXT NOT NULL,
        user_2 TINYTEXT NOT NULL,
        UNIQUE(user_1, user_2)
    );
"""

CREATE_MESSAGES_TABLE = """
    CREATE TABLE messages (
        relationship_id INT NOT NULL,
        sender TINYTEXT NOT NULL,
        sent timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        message TEXT NOT NULL,
        FOREIGN KEY (relationship_id)
            REFERENCES partners(relationship_id) ON DELETE CASCADE
    );
"""

CREATE_PARTNER_RELATIONSHIP = """
    INSERT IGNORE INTO `partners` VALUES (NULL, ?, ?);
"""

GET_PARTNER_ID = """
    SELECT `relationship_id` from partners where `user_1` = ? and `user_2` = ?;
"""

WRITE_MESSAGE = """
    INSERT INTO `messages` VALUES (?, ?, NULL, ?);
"""

GET_MESSAGES = """
    SELECT sender, message, sent FROM messages WHERE sent < ? AND relationship_id = ? LIMIT ?;
"""

GET_RECENT_MESSAGES = """
    SELECT sender, message, sent FROM messages WHERE sent < ? LIMIT ?;
"""


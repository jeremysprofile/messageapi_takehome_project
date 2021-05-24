/* our environment variable in docker-compose takes care of this for us.
 CREATE DATABASE messageapi;
 USE messageapi;
*/
CREATE TABLE partners (
    relationship_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_1 TINYTEXT NOT NULL,
    user_2 TINYTEXT NOT NULL,
    UNIQUE(user_1, user_2)
);

CREATE TABLE messages (
    relationship_id INT NOT NULL,
    sender TINYTEXT NOT NULL,
    sent timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    message TEXT NOT NULL,
    FOREIGN KEY (relationship_id)
        REFERENCES partners(relationship_id) ON DELETE CASCADE
);

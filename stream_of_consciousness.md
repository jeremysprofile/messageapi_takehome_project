## Stream of Consciousness Architecture
This is not useful for end users.

### API
So the api is stupid simple, right?

```
POST {msg} api/v1/send/{user}/{partner}  # records timestamp
GET api/v1/retrieve/{user}/{partner}/?quantity={quantity}&after={timestamp}  # query parameters are optional with defaults
```

Timestamp is just UTC; timestamp conversions are for frontends.
We don't have to delete (these are text messages we can ~~data harvest~~ save for prosperity).
We don't have to update (it's an IM, you don't edit).

We can do default values somehow probably, and the frontend can figure out how they want to turn some sort of pagination into infinite doomscrolling.

### DB
So... SQL? I don't know NoSQL, so yes. (I also don't know SQL.)

So, I want a user table that maps key, user, and a list of partners?
[No, lists are bad](https://stackoverflow.com/questions/3070384/how-to-store-a-list-in-a-column-of-a-database-table).

So I point to a table for this user and it has a bunch of rows for the conversation partners?

And each row is parter and conversation table?
And each conversation table is timestamp, sending user, text message content?

I guess.
So our partner rows have some duplicate data (partner is a two-way street), who cares, this data is tiny.

### Updates?
So a normal thing an IM service needs is like auto-updating the frontend.
I really have no idea how do that. Buzzword buzzword websockets? Literally no idea.
I'm gonna ignore this.

## Stream of Consciousness Development

### DB
I really should know more SQL.
I really have no preference between Postgres and MariaDB so whatever, I'll use MariaDB, since it's more common at my work.

How do I make anything?

#### Docker
So let's make this run anywhere.
If I cared about image size, we could do better, but I don't (TODO add to TODO).
Jesus the Docker hub search is *terrible*, we'll just build what we want.
We could run things as not root, but I haven't had to bother.

I originally wanted to run all of this in one container (because it's one less command to stand up and honestly that's a valid metric to optimize for here) but it turns out it's kind of a pain to get python and a SQL server in one container.
I could have used SQLite which Flask basically comes with, but then it wouldn't be as persistent.

I just grabbed the [latest stable](https://hub.docker.com/_/mariadb) docker image.

```bash
docker run -p 3306:3306 --name message-db -e MARIADB_ROOT_PASSWORD=test -d mariadb:10.5
mysql -h 127.0.0.1 -u root -p
```

This took over an hour. I should learn SQL better.
```sql
CREATE DATABASE messageapi;
USE messageapi;

CREATE TABLE usernames (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username CHAR(15) NOT NULL
);
CREATE TABLE partners (
  partner_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id_1 INT NOT NULL,
  user_id_2 INT NOT NULL,
  FOREIGN KEY (user_id_1)
    REFERENCES usernames(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id_2)
    REFERENCES usernames(id) ON DELETE CASCADE
);
CREATE TABLE messages (
  id INT NOT NULL auto_increment primary key,
  sent timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  sender INT NOT NULL,
  FOREIGN KEY (sender)
    REFERENCES usernames(id) ON DELETE CASCADE
);
```

### Dockerize

Now we make the python container.
I originally tried Alpine, then gave up after 10 min of trying to find all the dependencies for `cryptography`.
```bash
# alias for 'gimme a shell in that image'
drunsh python:3.9-buster
wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
echo "9f73807c80d14930494021d23abc222c9dd5a1c2731510a2b4d0f835fcc0ae4e mariadb_repo_setup" \
    | sha256sum -c -
chmod +x mariadb_repo_setup
./mariadb_repo_setup \
   --mariadb-server-version="mariadb-10.5" --skip-check-installed
apt update
apt upgrade -y
pip3 install poetry mariadb
```

Cool, now we have a working ... workspace.

I made a `Dockerfile` for the python image.

Found out that Docker images need [a network to communicate over](https://stackoverflow.com/a/42321366/5889131).

I also found a [quick tutorial](https://hackernoon.com/getting-started-with-mariadb-using-docker-python-and-flask-pa1i3ya3) on getting mariadb and flask set up together.

Time: 4hr. That sucks, huh?

### Docker Compose
Turns out [the basic tutorial](https://docs.docker.com/compose/gettingstarted/) is really all I needed to get `docker-compose up` working. Neat.
As a bonus, we don't need the network to communicate over, since compose uses one by default.
Also I guess it's called `docker compose up` according to log info when I run `docker-compose up` even though the tutorial says otherwise. Sure.

Also the Docker Compose version of [healthchecks](https://docs.docker.com/compose/startup-order/) are straight garbage so you have to just add it to the container that has a dependency on another container.

Testing was a little hard because:

* The docker image wouldn't update, so I had to run [`docker-compose down -v --rmi local`](https://github.com/docker/compose/issues/3472#issuecomment-220165334) before the next `docker compose up`.
*  Sometimes I wanted to manually run the image in docker and add it to the network, which I could do with `docker run --net messageapi_default --name testpants -p 8080:5000 --rm test:jeremy` after building it.

### Flask
Let's learn [flask](https://flask.palletsprojects.com/en/2.0.x/tutorial/).

I didn't know that I needed to set `host='0.0.0.0'` and wasted 2 hours trying to figure out why I couldn't hit a flask port through Docker.




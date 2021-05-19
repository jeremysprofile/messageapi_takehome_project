import flask
import logging
from .database_connection import DatabaseConnection


app = flask.Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello, World!'


def main():
    setup_logging()
    with DatabaseConnection() as db:
        db.db_setup()
    logging.info("starting flask")
    # I spent 2 hours figuring out that I needed host='0.0.0.0' in a Docker container, so that's fun
    app.run(host='0.0.0.0')


def setup_logging():
    formatter = logging.Formatter(
        "{asctime} {levelname:8s} ({filename}:{lineno})- {message}",
        style="{",
    )
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.StreamHandler().setFormatter(formatter)
    logging.debug("logging set up")


if __name__ == "__main__":
    main()

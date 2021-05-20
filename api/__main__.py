import flask
import logging
from .database_connection import DatabaseConnection
from flask import request, jsonify


app = flask.Flask(__name__)


@app.route('/api/v1')
def hello():
    logging.info(request.args)
    logging.info(request)
    # There's probably some cool flask way to auto-document this and have the docs keep up with the code.
    # But I don't know flask.
    return {
        "endpoints": {
            '/api/v1/send/{user}/{partner}': {
                'method': 'POST',
                'content-type': 'application/json',
                'body': {
                    'keys': {
                        'message': "The contents of the message to be sent."
                    }
                },
                'description': (
                    "Writes the {message} to the database from "
                    "{user} to {partner} with timestamp of time received."
                ),
            },
            '/api/v1/query/?count={count}&timestamp={timestamp}': {
                'method': 'GET',
                'response-type': 'application/json',
                'response-format': "[{'message': {message}, 'sender': {sender}, 'timestamp': {timestamp}},...]",
                'description': (
                    "Returns <={count} messages that were sent after {timestamp} "
                    "in the format described by {response-format}."
                ),
            },
            '/api/v1/query/{user}/{partner}?count={count}&timestamp={timestamp}': {
                'method': 'GET',
                'response-type': 'application/json',
                'response-format': "[{'message': {message}, 'sender': {sender}, 'timestamp': {timestamp}},...]",
                'description': (
                    "Returns <={count} messages that were sent after {timestamp} between "
                    "{user} and {partner} in the format described by {response-format}."
                ),
            },
        },
        "parameters": {
            "user": "Username. <255 latin1 characters. User auto-created when used.",
            "partner": "Recipient username. <255 latin1 characters. Recipient auto-created when used.",
            "count": "Limit number of returned messages. Integer. Defaults to no limit.",
            "timestamp": "Limit messages to those after timestamp. Defaults to no limit.",
            "message": "Sent message. <65535 latin1 characters.",
            "sender": "Sender. <255 latin1 characters. Will be one of the two usernames in the conversation."
        }
    }


@app.route('/api/v1/send/<user>/<partner>', methods=['POST', 'GET'])
def send():
    if request.method == 'GET':
        # TODO docs here
        pass
    if request.method == 'POST':
        # does the user exist?

        pass

    return 'Hello, World!'


@app.route('/api/v1/query/<user>/<partner>', methods=['POST', 'GET'])
def query():
    if request.method == 'GET':
        # TODO docs here
        pass
    if request.method == 'POST':
        # does the user exist?

        pass

    return 'Hello, World!'


@app.route('/api/v1/query', methods=['POST', 'GET'])
def query_all():
    if request.method == 'GET':
        # TODO docs here
        pass
    if request.method == 'POST':
        # does the user exist?

        pass

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

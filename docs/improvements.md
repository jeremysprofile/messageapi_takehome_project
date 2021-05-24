# Improvements

## Performance
* Use a production-ready webserver, as ["Flask’s built-in server is not suitable for production"](https://flask.palletsprojects.com/en/2.0.x/deploying/)
* Create multiple instances of the Flask container and put them behind a load balancer
* Sharded database with multiple MariaDB containers
* Allocate more resources to containers via a multi-node cluster (either Docker Swarm or Kubernetes)
* Read replicas of the DB

## Architecture
This is not a good architecture for messaging.
Currently, the frontend is required to periodically request messages between the user and any partner (which it can do
via requesting only new messages since the last timestamp of interaction with the backend for that user-partner
relationship).
If we only want to alert the user to new messages on chat windows they currently have up, this may be reasonable, but it
does not provide the ability to be notified of a new message from a new sender.

A better design would be using websockets ... somehow. Unfortunately, I've never used websockets, and this project
already took way over the 4 hours Guild told me to allocate, so here we are.

## Resiliency
* Persistent storage volumes rather than ephemeral container storage
* Make containers auto-restart on failure
* Multi-node cluster (either Docker Swarm or Kubernetes)
* Logging and monitoring

## Codebase
Use `black`, `isort`, `mypy`, and `pylint` to lint and style-check the code.
Write tests in `pytest`. Ran out of time to do this.

# Take-home project - Guild
* [Requirements](./docs/requirements.md)

## Development Process
See [`stream_of_consciousness.md`](./docs/stream_of_consciousness.md)

Once things actually connected, it was editing the python code and running the following line over and over:
```bash
docker compose up; docker-compose down -v --rmi local
```
And sometimes having the following in another terminal for double-checking:
```bash
mysql -h 127.0.0.1 -u root -pguild -D messageapi
```

## Install
1. Make sure you have Docker (only tested on Docker Desktop for Mac - download it [here](https://www.docker.com/products/docker-desktop)).
2. Clone this repo:
```bash
git clone git@github.com:jeremysprofile/messageapi_takehome_project.git
```

## Run
```bash
cd messageapi_takehome_project/  # the dir where this README is
docker compose up
```

The api is available at `localhost:80/api/v1/`. `GET localhost:80/api/v1/` describes the endpoints.

## Future Improvements
See [`improvements.md`](./docs/improvements.md)

## Caveats
I am honestly not sure whether it improves my application or not to say this, but this was my first time using Flask, Docker Compose, MariaDB via Python, or even writing a SQL schema.
This project took me roughly 20 hours, so 5x what was budgeted, but I did learn a lot and I feel good about the amount I was able to learn and accomplish.

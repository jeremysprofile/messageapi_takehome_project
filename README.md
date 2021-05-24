# Take-home project - Guild
* [Requirements](./docs/requirements.md)

## Development Process
See [`stream_of_consciousness.md`](./docs/stream_of_consciousness.md)

Once things actually connected, it was editing the python code and running the following line over and over:
```bash
docker compose up; docker-compose down -v --rmi local
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

## Future Improvements
See [`improvements.md`](./docs/improvements.md)

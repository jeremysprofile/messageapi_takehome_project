#!/bin/bash
. /venv/bin/activate 
# wait for mariadb to be available:
# stolen from https://stackoverflow.com/a/9609247/5889131
# why can't docker compose do this in a sane way?
# https://docs.docker.com/compose/startup-order/
# I guess this is why we use k8s
echo 'Waiting for DB to become available'
while [[ -z "$stop" ]]; do
  exec 6<>/dev/tcp/message-db/3306 && stop='yeah port is listening now'
  exec 6>&- # close output connection
  exec 6<&- # close input connection
  sleep 1
  echo 'DB still not up'
done
# god this is a garbage healthcheck
sleep 2
echo 'DB up'
python -m api

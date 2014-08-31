#!/usr/bin/env bash

# Instructions:
#
# run from project root directory

# Make sure the docker image is up to date
make build

docker run --detach --name elevators-wsgi --link pgplus:postgis \
  --env-file env-docker -p 8000 texastribune/elevators \
  gunicorn example_project.wsgi --bind 0.0.0.0:8000 --log-file -
MANAGE="python ./example_project/manage.py"
PORT=$(docker port elevators-site 8000 | cut -d : -f 2)

# give time for the servers to get up
sleep 1

mkdir -p site
cd site && wget -r localhost:$PORT --force-html -e robots=off -nH -nv --max-redirect 0

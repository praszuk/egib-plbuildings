#!/bin/bash

if [ "$INSIDE_DOCKER" == "1" ]; then
  pytest -s -p no:cacheprovider "$@"
else
  docker compose -f docker-compose-dev.yml run -i --rm -e INSIDE_DOCKER=1 backend backend/test.sh "$@"
fi

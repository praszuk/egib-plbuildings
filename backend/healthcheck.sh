#!/bin/bash
docker compose -f docker-compose-prod.yml exec -it backend bash -c "python backend/tests/expected_buildings_hc.py $@"
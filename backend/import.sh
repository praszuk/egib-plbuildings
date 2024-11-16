#!/bin/bash
docker compose -f docker-compose-prod.yml exec -it backend bash -c "python backend/tasks/import_buildings.py $@"
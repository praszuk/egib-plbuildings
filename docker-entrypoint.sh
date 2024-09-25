#!/bin/bash
# Start server
echo "Starting server"
uvicorn backend.main:app $( (( $DEV == 1 )) && printf %s '--reload' ) --host 0.0.0.0 --port 8000 --log-config backend/core/log_config.yaml --forwarded-allow-ips=*

#!/bin/sh
set -e

echo "=== Starting Mini Social Backend ==="

# Wait for PostgreSQL
echo "Waiting for PostgreSQL at ${DB_HOST:-db}:${DB_PORT:-5432}..."
python << 'EOF'
import socket
import time
import os
import sys

host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "5432"))

start_time = time.time()
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"Connected to PostgreSQL successfully at {host}:{port}")
            sys.exit(0)
    except (socket.error, ConnectionRefusedError, TimeoutError):
        time.sleep(1)
        if time.time() - start_time > 60:
            print(f"Timed out waiting for PostgreSQL at {host}:{port}")
            sys.exit(1)
EOF

# Wait for Redis if configured
if [ -n "$REDIS_HOST" ]; then
  echo "Waiting for Redis at ${REDIS_HOST}:${REDIS_PORT:-6379}..."
  python << 'EOF'
import socket
import time
import os
import sys

host = os.getenv("REDIS_HOST", "redis")
port = int(os.getenv("REDIS_PORT", "6379"))

start_time = time.time()
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"Connected to Redis successfully at {host}:{port}")
            sys.exit(0)
    except (socket.error, ConnectionRefusedError, TimeoutError):
        time.sleep(1)
        if time.time() - start_time > 60:
            print(f"Timed out waiting for Redis at {host}:{port}")
            sys.exit(1)
EOF
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Backend initialization complete. Executing command..."
exec "$@"

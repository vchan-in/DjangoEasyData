#!/bin/bash

echo "Waiting for MySQL to be available..."

# Set the MySQL host and port (change if needed)
MYSQL_HOST="${MYSQL_HOST:-mysql}"
MYSQL_PORT="${MYSQL_PORT:-3306}"

# Wait until MySQL is reachable
while ! nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
  sleep 1
  echo "Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."
done

echo "MySQL is up!"
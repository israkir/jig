#!/usr/bin/env bash
# First boot of an empty Postgres volume. Creates one role, one database, and one schema.
set -euo pipefail

name="${APP_DB_NAME:?APP_DB_NAME is required}"
pass="${APP_DB_PASSWORD:?APP_DB_PASSWORD is required}"

if [[ ! "$name" =~ ^[a-z][a-z0-9_]*$ ]]; then
  echo "APP_DB_NAME must match ^[a-z][a-z0-9_]*$" >&2
  exit 1
fi

sql_pass="${pass//\'/\'\'}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<SQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '${name}') THEN
    CREATE ROLE ${name} LOGIN PASSWORD '${sql_pass}';
  END IF;
END
\$\$;
SELECT 'CREATE DATABASE ${name} OWNER ${name}'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${name}')\gexec
SQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "${name}" \
  -c "CREATE SCHEMA IF NOT EXISTS ${name} AUTHORIZATION ${name};"

echo "[init] role+db ready: ${name}"

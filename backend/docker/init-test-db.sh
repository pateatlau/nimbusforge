#!/bin/sh
set -eu

psql --set=ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    --set=test_db="$POSTGRES_TEST_DB" <<'SQL'
SELECT format('CREATE DATABASE %I', :'test_db') \gexec
SQL
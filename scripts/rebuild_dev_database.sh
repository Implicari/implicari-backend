#!/bin/bash


PGPASSWORD=$DATABASE_PASSWORD psql -h $DATABASE_HOST -U $DATABASE_USER -p $DATABASE_PORT \
    -c "DROP DATABASE $DATABASE_NAME;"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

$DIR/build_dev_database.sh

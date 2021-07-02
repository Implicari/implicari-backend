#!/bin/bash


TENANT="dev"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

PGPASSWORD=$DATABASE_PASSWORD psql -h $DATABASE_HOST -U $DATABASE_USER -p $DATABASE_PORT \
    -c "CREATE DATABASE $DATABASE_NAME;"

python manage.py migrate

python manage.py create_tenant --name home --schema_name public --domain-domain localhost --domain-is_primary True
python manage.py create_tenant --name $TENANT --schema_name $TENANT --domain-domain $TENANT.localhost --domain-is_primary False

python manage.py tenant_command loaddata $DIR/../fixtures/persons.fake.json -s $TENANT

echo "Create super user for $TENANT tenant"
pipenv run python manage.py create_tenant_superuser \
    -s $TENANT \
    --email admin@$TENANT.localhost \
    --person_id 1 \
    --password password \
    --no-input

python manage.py tenant_command loaddata $DIR/../fixtures/classrooms.fake.json -s $TENANT

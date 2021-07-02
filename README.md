# Implicari Backend

[![Coverage Status](https://coveralls.io/repos/github/ByteRockCode/implicari-backend/badge.svg?branch=master)](https://coveralls.io/github/ByteRockCode/implicari-backend?branch=master)
[![Build Status](https://travis-ci.org/ByteRockCode/implicari-backend.svg?branch=master)](https://travis-ci.org/ByteRockCode/implicari-backend)


## Installation

### Requerimientos

- Git
- Docker
- Pyenv
- PDM


### Clonar repositorio

```bash
mkdir -p ~/Dev/ByteRock
cd ~/Dev/ByteRock
git clone git@github.com:ByteRockCode/implicari-backend.git
```


### Dependencias

```bash
cd implicari-backend
pdm install
```


### Base de datos

```bash
docker volume create implicari-postgres
docker container create --name implicari-postgres --volume implicari-postgres:/var/lib/postgresql/data -e POSTGRES_PASSWORD=password -p 5432:5432 postgres
docker container start implicari-postgres
docker exec -it implicari-postgres createdb -U postgres implicari
```


## Virtualenv

Create file `.env`

```env
ALLOWED_HOSTS=*
DATABASE_URL=postgres://postgres:password@localhost:5432/implicari
DJANGO_SETTINGS_MODULE=config.settings.development
ENV=development
SECRET_KEY=123456
DEBUG_TOOLBAR=True

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=25
```


## Creación de tablas y datos iniciales


```bash
pdm run python manage.py migrate

pdm run python manage.py create_tenant --name home --schema_name public --domain-domain localhost --domain-is_primary True

pdm run python manage.py create_tenant --name dev --schema_name dev --domain-domain dev.localhost --domain-is_primary False

pdm run python manage.py tenant_command loaddata fixtures/persons.fake.json -s dev

pdm run python manage.py create_tenant_superuser \
    -s dev \
    --email admin@dev.localhost \
    --person_id 1 \
    --password password \
    --no-input

pdm run python manage.py tenant_command loaddata fixtures/classrooms.fake.json -s dev
```


## Iniciar servidor

```
pdm run python manage.py runserver 0.0.0.0:8000
```

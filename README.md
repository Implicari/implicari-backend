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
DATABASE_URL=postgres://postgres:password@localhost:5432/implicari

DEBUG=True
SECRET_KEY=123456

DJANGO_DEBUG_TOOLBAR_ENABLED=True
DJANGO_EXTENSIONS_ENABLED=True

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=25
```


## Creación de tablas y datos iniciales


```bash
pdm run python manage.py migrate

pdm run python manage.py loaddata fixtures/persons.fake.json

pdm run python manage.py create_superuser \
    --email admin@localhost \
    --person_id 1 \
    --password password \
    --no-input

pdm run python manage.py loaddata fixtures/classrooms.fake.json
```


## Iniciar servidor

```
pdm run python manage.py runserver 0.0.0.0:8000
```

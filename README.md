# Implicari Backend

[![Coverage Status](https://coveralls.io/repos/github/ByteRockCode/classroom-backend/badge.svg?branch=master)](https://coveralls.io/github/ByteRockCode/classroom-backend?branch=master)
[![Build Status](https://travis-ci.org/ByteRockCode/classroom-backend.svg?branch=master)](https://travis-ci.org/ByteRockCode/classroom-backend)

## Installation

```bash
mkdir -p ~/Dev/ByteRock
cd ~/Dev/ByteRock
git clone git@github.com:ByteRockCode/classroom-backend.git

cd classroom-backend
pipenv install --dev
sh scripts/database_build.sh
```


## Virtualenv

Create file `.env`

```
ALLOWED_HOSTS='*'
DATABASE_URL='postgres://postgres@localhost:5432/classroom'
DJANGO_SETTINGS_MODULE='config.settings.development'
ENV='development'
SECRET_KEY='123456'
DEBUG_TOOLBAR=True

EMAIL_HOST=''
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
EMAIL_PORT=25

```


## Run server

```
pipenv run python manage.py runserver 0.0.0.0:8000
```

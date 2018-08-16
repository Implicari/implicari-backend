#!/bin/sh

python manage.py loaddata fixtures/users.fake.json
python manage.py loaddata fixtures/classrooms.fake.json

mkdir -p media/fixtures/
cp -r fixtures/media/* media/fixtures/

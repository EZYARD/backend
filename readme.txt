TO RUN THE BACKEND:
===================

PYTHON VERSION REQUIRED: 3.11.0

pip install virtualenv
virtualenv --python=/path/to/python3.11 venv
venv\Scripts\activate

once ready:

pip install -r requirements.txt

cd into /backend

run
fastapi dev main.py

RUNNING DB:
===========

cd db
docker-compose up -d
alembic upgrade head


db url on local: postgresql+psycopg2://myuser:mypassword@localhost:5432/mydb


CREATING A REVISION TO THE DB
=============================

step 1.
alembic revision -m "My revision Message"
step 2.
under db/alembic/versions, find the revision file. To create a revision file,
use db/alembic/versions/9017eb6eb0fd_create_users_table.py as an example
step 3.
After creating your revision file, run the migration to the db by running
alembic upgrade head
step 4.
Test the db on postbird by connecting to it and seeing if the new table/columns were added


profit :)
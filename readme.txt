TO RUN THE BACKEND:

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

cd db
docker-compose up -d
alembic upgrade head

profit :)
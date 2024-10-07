from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Initialize FastAPI app
app = FastAPI()

# Replace with your database URL (adjust for your DB: PostgreSQL, MySQL, SQLite, etc.)
DATABASE_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5432/mydb"

# Create an engine and connect to the database
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Reflect the existing database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Get the user table
user_table = Table('users', metadata, autoload_with=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Route to fetch user data
@app.get("/users")
async def get_users():
    # Fetch users data
    with engine.connect() as connection:
        query = user_table.select()
        result = connection.execute(query)

        # Convert the result into a list of dictionaries (JSON-friendly format)
        users = [dict(row._mapping) for row in result]  # Use row._mapping to convert to dict

    return {"users": users}


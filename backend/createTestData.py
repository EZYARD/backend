from sqlalchemy import create_engine, MetaData, Table, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from constants import DATABASE_URL

# Replace with your actual database URL

# Define engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Reflecting the table from the database
metadata = MetaData()
metadata.reflect(bind=engine)
listings = metadata.tables['listings']

# Test data to insert (U.S. Presidents)
test_data = [
    {
        'name': 'George Washington',
        'streetNumber': '1',
        'streetName': 'Mount Vernon',
        'city': 'Fairfax County',
        'state': 'VA',
        'zipcode': 22121,
        'description': 'First president of the United States, known for setting the foundation of American government.',
        'startTime': datetime(1789, 4, 30),
        'endTime': datetime(1797, 3, 4),
        'tags': 'founding father, independence, leadership',
        'priceRange': 5,
        'rating': 5,
        'reviews': 'The father of the country, an unparalleled leader.'
    },
    {
        'name': 'Abraham Lincoln',
        'streetNumber': '1600',
        'streetName': 'Pennsylvania Avenue NW',
        'city': 'Washington',
        'state': 'DC',
        'zipcode': 20500,
        'description': '16th president, led the country through the Civil War and abolished slavery.',
        'startTime': datetime(1861, 3, 4),
        'endTime': datetime(1865, 4, 15),
        'tags': 'civil war, emancipation, leadership',
        'priceRange': 5,
        'rating': 5,
        'reviews': 'The Great Emancipator, a transformative figure.'
    },
    {
        'name': 'Franklin D. Roosevelt',
        'streetNumber': '1600',
        'streetName': 'Pennsylvania Avenue NW',
        'city': 'Washington',
        'state': 'DC',
        'zipcode': 20500,
        'description': '32nd president, led the U.S. through the Great Depression and World War II.',
        'startTime': datetime(1933, 3, 4),
        'endTime': datetime(1945, 4, 12),
        'tags': 'new deal, world war ii, leadership',
        'priceRange': 5,
        'rating': 5,
        'reviews': 'A president who brought the country through its darkest days.'
    },
    {
        'name': 'Barack Obama',
        'streetNumber': '1600',
        'streetName': 'Pennsylvania Avenue NW',
        'city': 'Washington',
        'state': 'DC',
        'zipcode': 20500,
        'description': '44th president, first African American president of the United States.',
        'startTime': datetime(2009, 1, 20),
        'endTime': datetime(2017, 1, 20),
        'tags': 'affordable care act, leadership, change',
        'priceRange': 5,
        'rating': 5,
        'reviews': 'A president who inspired hope and change.'
    },
    {
        'name': 'Joe Biden',
        'streetNumber': '1600',
        'streetName': 'Pennsylvania Avenue NW',
        'city': 'Washington',
        'state': 'DC',
        'zipcode': 20500,
        'description': '46th and current president, serving since 2021.',
        'startTime': datetime(2021, 1, 20),
        'endTime': datetime(2024, 1, 20),  # Still serving
        'tags': 'pandemic recovery, leadership, infrastructure',
        'priceRange': 5,
        'rating': 5,
        'reviews': 'Working to unite the country and address critical challenges.'
    }
]

# Inserting the test data into the listings table
with engine.connect() as conn:
    stmt = insert(listings).values(test_data)
    conn.execute(stmt)
    conn.commit()

print("Data about past and current presidents inserted successfully.")

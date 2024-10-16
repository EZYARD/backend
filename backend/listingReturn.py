import os
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData
from PIL import Image
#datetime import added to attempt to fix startTime and endTime

Base = declarative_base()

# Define the Listing model
class ListingModel(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    streetNumber = Column(Integer, nullable = False)
    streetName = Column(String, nullable = False)
    city = Column(String, nullable = False)
    state = Column(String, nullable = False)
    zipcode = Column(Integer, autoincrement = False, nullable = False)

    description = Column(String, nullable = False)

    #import datetime differently? ***
    #create datetime object? ***
    startTime = Column(DateTime, nullable = False)
    endTime = Column(DateTime, nullable = False)

    #stored as a comma separated list
    tags = Column(String, nullable = True)

    priceRange = Column(String, nullable = True)

    rating = Column(String, nullable = True)

    reviews = Column(String, nullable = True)
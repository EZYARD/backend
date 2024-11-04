from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Define the Listing model
class ListingModel(Base):
    uid = Column(String, nullable=True)
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    streetNumber = Column(Integer, nullable=False)
    streetName = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zipcode = Column(Integer, autoincrement=False, nullable=False)

    description = Column(String, nullable=False)

    # import datetime differently? ***
    # create datetime object? ***
    startTime = Column(DateTime, nullable=False)
    endTime = Column(DateTime, nullable=False)

    # stored as a comma separated list
    tags = Column(String, nullable=True)

    priceRange = Column(String, nullable=True)

    rating = Column(String, nullable=True)

    reviews = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
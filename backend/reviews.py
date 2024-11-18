from sqlalchemy import create_engine, Column, Integer,String, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class ReviewModel(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, nullable=False)
    review = Column(String, nullable=False)
    uid = Column(String, nullable=False)
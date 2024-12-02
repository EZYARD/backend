from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class UserData(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True)
    bookmarked_listings = Column(ARRAY(Integer), nullable=False)
    reviews_left = Column(ARRAY(Integer), nullable=False)
    uid = Column(String, nullable=False)
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

from src.database.db import engine

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(Date)
    extra_data = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
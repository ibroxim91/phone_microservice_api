from sqlalchemy import Column, Integer, String
from .base import Base


class Phone(Base):
    __tablename__ = "phones"
   
    phone = Column(String, unique=True, index=True)
    address = Column(String)

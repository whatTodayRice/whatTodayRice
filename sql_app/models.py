from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, unique=True)
    dormitory = Column(String, nullable=False)
    
    
    
    
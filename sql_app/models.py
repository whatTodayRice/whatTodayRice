from sqlalchemy import Column, Integer, Date, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, unique=True)
    dormitory = Column(String, nullable=False)
    
    
class Menu(Base):
    __tablename__="menu"
    menu_id =Column(Integer,primary_key=True)
    date = Column(String)
    breakfast=Column(String(500))
    takeout =Column(String,nullable=True)
    lunch = Column(String)
    dinner=Column(String)
    
class SejongMenu(Base):
    __tablename__="sejong_menu"
    menu_id =Column(Integer,primary_key=True)
    date = Column(String)
    breakfast=Column(String(500))
    lunch = Column(String)
    dinner=Column(String)
    
    
    
from sqlalchemy.orm import Session
from sql_app import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Date


'''
사용자 
1. 생성
2. 전체 조회
3. id만 조회
'''

def create_user(db:Session, user_id: str, dormitory:str):
    db_user = models.User(user_id=user_id, dormitory=dormitory)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user

def read_user(db:Session, user_id:str):
    return (
    db.query(models.User).filter(models.User.user_id == user_id).first()
    )

# 행복 저장
def save_menu(db:Session,date:str,breakfast:str,takeout:str, lunch:str,dinner:str):
    db_menu = models.Menu(date=date,breakfast=breakfast,takeout=takeout,lunch=lunch,dinner=dinner)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def read_happy_menu(db:Session, date:str):
    return(
    db.query(models.Menu).filter(models.Menu.date == date).first()
    )

# 세종 저장 
def save_sejong_menu(db:Session,date:str,breakfast:str, lunch:str,dinner:str):
    db_menu = models.SejongMenu(date=date,breakfast=breakfast,lunch=lunch,dinner=dinner)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def read_sejong_menu(db:Session, date:str):
    return(
    db.query(models.SejongMenu).filter(models.SejongMenu.date == date).first()
    )
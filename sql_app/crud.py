from sqlalchemy.orm import Session
from sql_app import models

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

def get_user_by_user_id(db:Session,user_id:str):
    return (
	db.query(models.User).filter_by(user_id=user_id).first()
    )
from sqlalchemy.orm import Session
from sql_app import models

def create_user(db:Session, user_id: str, dormitory:str):
    db_user = models.User(user_id=user_id, dormitory=dormitory)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return db_user

def get_user_by_user_id(db:Session, user_id:str):
    return (
    db.query(models.User).filter(models.User.user_id == user_id).first()
    )

def check_user_by_user_id(db:Session,user_id:str):
    return (
	db.query(models.User).filter_by(user_id=user_id).first()
    )
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from meal_model.happy import Happy
from meal_model.sejong import Sejong
from typing import Dict
from sql_app import crud, database, models
from sql_app.database import SessionLocal,engine
from sql_app.crud import create_user,read_user
from error_handler import Homepage
from template import KakaoTemplate
from fastapi.responses import JSONResponse
from datetime import datetime, timezone, timedelta


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ResponseBody(BaseModel):
    version: str
    template: dict


global sejongUrl 
sejongUrl= "https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php"
global happyUrl 
happyUrl= "https://happydorm.or.kr/busan/ko/0606/cafeteria/menu"


''' 
	사용자 및 기숙사 정보 등록 
'''

@app.post("/registerUserAndDormitory")
def register_user_dormitory(response: Dict, db:Session = Depends(get_db)):
    user_id = response['userRequest']['user']['properties']['plusfriend_user_key']
    
    #userId 가 이미 있는지 검사
    user = crud.read_user(db,user_id=user_id)
    if user:
        return KakaoTemplate.build_dormitory_text("이미 등록된 사용자입니다.")
    else:
        dormitory=response['action']['clientExtra']['Dormitory_item']
        create_user(db = db, user_id=user_id, dormitory=dormitory)
        register_dormitory = dormitory+"기숙사로 등록되었습니다."
        return KakaoTemplate.build_dormitory_text(register_dormitory)
    
''' 
	기숙사 정보 수정
'''   
@app.post("/updateDormitory")
def update_dormitory(response: Dict, db:Session = Depends(get_db)):
    user_id = response['userRequest']['user']['properties']['plusfriend_user_key']
    dormitory=response['action']['clientExtra']['Dormitory_item']
    print(user_id)
    user = crud.read_user(db,user_id=user_id)
    
    if(user.dormitory!=dormitory):
        user.dormitory=dormitory
        db.commit()
        modify_dormitory = dormitory+"기숙사로 수정되었습니다."
        return KakaoTemplate.build_dormitory_text(modify_dormitory)
    else:
        notify_dormitory = dormitory + "로 이미 등록되어있습니다."
        return KakaoTemplate.build_dormitory_text(notify_dormitory)
    
    
'''
	오늘,내일,주간 식단받아오는 코드 
'''

Sejong = Sejong()
Happy = Happy()

@app.post("/todayMenu", response_model=None)
def fetch_today_menu(content: dict, db:Session = Depends(get_db)):

    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user =crud.read_user(db,user_id=user_id)
    
    if (user.dormitory == "세종"):
        sejong_today_menu = Sejong.fetch_today_menu(db)
        return KakaoTemplate.build_menu_text(sejong_today_menu)
    if (user.dormitory == "행복"):
        happy_today_menu = Happy.fetch_today_menu(db)
        return KakaoTemplate.build_menu_text(happy_today_menu)
       
    
@app.post("/tomorrowMenu", response_model=None)
def fetch_tomorrow_menu(content: dict, db:Session = Depends(get_db)):
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.read_user(db,user_id=user_id)
    
    if (user.dormitory == "세종"):
        sejong_tomorrow_menu = Sejong.fetch_tomorrow_menu(db)
        return KakaoTemplate.build_menu_text(sejong_tomorrow_menu)
    if (user.dormitory == "행복"):
        happy_tomorrow_menu = Happy.fetch_tomorrow_menu(db)
        return KakaoTemplate.build_menu_text(happy_tomorrow_menu)


@app.post("/weekMenu", response_model=None)
def fetch_week_menu(content: dict, db:Session = Depends(get_db)):
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.read_user(db,user_id=user_id)
    
    
    if (user.dormitory =="세종"):
        sejong_week_menu = Sejong.fetch_week_menu(db,content)
       	return KakaoTemplate.build_menu_text(sejong_week_menu)
        
    else:
        happy_week_menu = Happy.fetch_week_menu(db,content)
        return KakaoTemplate.build_menu_text(happy_week_menu)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2000)

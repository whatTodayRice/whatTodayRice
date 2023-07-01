from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from meal_model.happy import Happy
from meal_model.sejong import Sejong
from typing import Dict
from sql_app import crud, database, models
from sql_app.database import SessionLocal,engine
from sql_app.crud import create_user,read_user
from template import KakaoTemplate
from datetime import datetime, timezone, timedelta
from constants import Constants

from scrap_save_menu.both_dormitory import ScrapAndSave
from scrap_save_menu.sejong_sat import SejongSatMenu

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

''' 
	사용자 및 기숙사 정보 등록 
'''

@app.post("/registerUserAndDormitory")
def register_user_dormitory(response: Dict, db:Session = Depends(get_db)):
    user_id = response['userRequest']['user']['properties']['plusfriend_user_key']
    dormitory=response['action']['clientExtra']['Dormitory_item']
    user = crud.read_user(db,user_id=user_id)
    dormitory_resister_confirm_text = f"✅ {dormitory} 기숙사로 등록되었습니다.\n😊 아래 버튼을 눌러 {dormitory} 식단을 받아보세요!"
    
    # 유저 없는 경우
    if user is None:
        create_user(db = db, user_id=user_id, dormitory=dormitory)
        return KakaoTemplate.build_simple_text(dormitory_resister_confirm_text)
    
    else:
        # 잘못등록
        if (user.dormitory!=dormitory):
            user.dormitory=dormitory
            db.commit()
            return KakaoTemplate.build_simple_text(dormitory_resister_confirm_text)
        # 동일등록
        else:
        	return KakaoTemplate.build_simple_text(dormitory_resister_confirm_text)
    
'''
	오늘,내일,주간 식단받아오는 코드 
'''

Sejong = Sejong()
Happy = Happy()

@app.post("/todayMenu", response_model=None)
def fetch_today_menu(content: dict, db:Session = Depends(get_db)):

    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user =crud.read_user(db,user_id=user_id)
    
    # user가 None이면 -> 기숙사등록하기 멘트 및 바로가기 버튼 
    if user == None:
        return KakaoTemplate.build_register_dormitory_text(Constants.dormitory_register_request_text)
    
    if (user.dormitory == "세종"):
        # ScrapAndSave.sejong_scrap_save_menu()
        # SejongSatMenu.scrap_save_Sat_menu()
        sejong_today_menu = Sejong.fetch_today_menu(db)
        if sejong_today_menu:
            return KakaoTemplate.build_simple_text(sejong_today_menu)
        else: 
            return KakaoTemplate.build_no_menu_text(Constants.inform_not_update_menu_text)
            
    if (user.dormitory == "행복"):
        # ScrapAndSave.happy_scrap_save_menu()
        happy_today_menu = Happy.fetch_today_menu(db)
        if happy_today_menu:
            return KakaoTemplate.build_simple_text(happy_today_menu)
        else: 
             return KakaoTemplate.build_no_menu_text(Constants.inform_not_update_menu_text)
       
@app.post("/tomorrowMenu", response_model=None)
def fetch_tomorrow_menu(content: dict, db:Session = Depends(get_db)):
    
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.read_user(db,user_id=user_id)
    
    if user == None:
        return KakaoTemplate.build_register_dormitory_text(Constants.dormitory_register_request_text)
    
    if (user.dormitory == "세종"):
        sejong_tomorrow_menu = Sejong.fetch_tomorrow_menu(db)
        if sejong_tomorrow_menu:
            return KakaoTemplate.build_simple_text(sejong_tomorrow_menu)
        else:
            return KakaoTemplate.build_no_menu_text(Constants.inform_not_update_menu_text)
    if (user.dormitory == "행복"):
        happy_tomorrow_menu = Happy.fetch_tomorrow_menu(db)
        if happy_tomorrow_menu:
            return KakaoTemplate.build_simple_text(happy_tomorrow_menu)
        else:
            return KakaoTemplate.build_no_menu_text(Constants.inform_not_update_menu_text)


@app.post("/weekMenu", response_model=None)
def fetch_week_menu(content: dict, db:Session = Depends(get_db)):
    
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.read_user(db,user_id=user_id)
    
    if user == None:
        return KakaoTemplate.build_register_dormitory_text(Constants.dormitory_register_request_text)
    
    if (user.dormitory == "세종"):
        sejong_week_menu = Sejong.fetch_week_menu(db,content)
        if sejong_week_menu:
            return KakaoTemplate.build_simple_text(sejong_week_menu)
        else: 
            return KakaoTemplate.build_no_menu_text(Constants.inform_not_update_menu_text)
            
    if (user.dormitory == "행복"):
        happy_week_menu = Happy.fetch_week_menu(db,content)
        if happy_week_menu:
            return KakaoTemplate.build_simple_text(happy_week_menu)
        else: 
             return KakaoTemplate.build_no_menu_text(Constants.inform_not_update_menu_text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2000)
    
    

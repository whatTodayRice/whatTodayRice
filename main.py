from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from mealModel import MealModel
from typing import Dict
from sql_app import crud, database, models
from sql_app.database import SessionLocal,engine
from sql_app.crud import create_user,read_user,get_user_by_user_id
from error_handler import Homepage
from template import KakaoTemplate
from fastapi.responses import JSONResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
meal = MealModel()

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
    user = read_user(db,user_id=user_id)
    if user:
        return KakaoTemplate.simple_text("이미 등록된 사용자입니다.")
    else:
        dormitory=response['action']['clientExtra']['Dormitory_item']
        create_user(db = db, user_id=user_id, dormitory=dormitory)
        register_dormitory = dormitory+"기숙사로 등록되었습니다."
        return KakaoTemplate.build_menu_text(register_alarm)
    
''' 
기숙사 정보 수정
'''   
@app.post("/updateDormitory")
def update_dormitory(response: Dict, db:Session = Depends(get_db)):
    user_id = response['userRequest']['user']['properties']['plusfriend_user_key']
    dormitory=response['action']['clientExtra']['Dormitory_item']
    user = crud.get_user_by_user_id(db,user_id=user_id)
    
    if(user.dormitory!=dormitory):
        user.dormitory=dormitory
        db.commit()
        modify_dormitory = dormitory+"기숙사로 수정되었습니다."
        return KakaoTemplate.build_dormitory_text(modify_dormitory)

'''
오늘,내일,주간 식단받아오는 코드 
'''
    
@app.post("/todayMenu", response_model=None)
def fetch_today_menu(content: dict, db:Session = Depends(get_db)):
    global sejongUrl 
    global happyUrl 
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user =crud.get_user_by_user_id(db,user_id=user_id)
    today_menu= meal.todayMenu()
    if (user.dormitory =="세종"):
        data = KakaoTemplate.build_menu_text(today_menu)
        return JSONResponse(content=data)
    
'''
행복 기숙사 식단 받아오는 코드 추가예정
'''
    
@app.post("/tommorowMenu", response_model=None)
def fetch_tommorow_menu(content: dict, db:Session = Depends(get_db)):
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.get_user_by_user_id(db,user_id=user_id)
    tommorow_menu= meal.todayMenu()
    if (user.dormitory =="세종"):
        data = KakaoTemplate.build_menu_text(tommorow_menu)
        return JSONResponse(content=data)

'''
행복 기숙사 식단 받아오는 코드 추가예정
'''

@app.post("/weekMenu", response_model=None)
def fetch_week_menu(content: dict, db:Session = Depends(get_db)):
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.get_user_by_user_id(db,user_id=user_id)
    week_menu = meal.weekMenu(content)
    if (user.dormitory =="세종"):
        data = KakaoTemplate.build_menu_text(week_menu)
        return JSONResponse(content=data)
        
'''
행복 기숙사 식단 받아오는 코드 추가예정
'''
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
    
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from mealModel import MealModel
from typing import Dict
from sql_app import crud, database, models
from sql_app.database import SessionLocal,engine
from sql_app.crud import create_user,get_user_by_user_id,check_user_by_user_id
from happy_menu import menu
from error_handler import Homepage
from template import KakaoTemplate


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


@app.get("/")
def read_root():
    return {"hello": 'World'}

global sejongUrl 
sejongUrl= "https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php"
global happyUrl 
happyUrl= "https://happydorm.or.kr/busan/ko/0606/cafeteria/menu"


@app.post("/todayMenu", response_model=None)
def fetch_today_menu(content: dict,db:Session = Depends(get_db)):
    global sejongUrl 
    global happyUrl 
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user =crud.get_user_by_user_id(db,user_id=user_id)
    
    response_body = ResponseBody(
        version="2.0",
        template={
            "outputs": [
                {
                    "simpleText": {
                        "text": meal.todayMenu()
                    }
                }
            ]
        }
    )
    return response_body
    
    
    
    # if(user.dormitory =="세종"):
    #     if not Homepage.checkConnection(sejongUrl):
    #         return Homepage.makeErrorMessage()
    #     else:
    #             response_body = ResponseBody(
    #                 version="2.0",
    #                 template={
    #                     "outputs": [
    #                         {
    #                 "simpleText": {
    #                     "text": meal.todayMenu()
    #                 }
    #             }
    #         ]
    #     }
    # )
    #             return response_body

    # else:
    #     if not Homepage.checkConnection(happyUrl):
    #         return Homepage.makeErrorMessage()
    #     else:
    #         response_body = ResponseBody(
    #             version="2.0",
    #             template={
    #                 "outputs": [
    #                 {
    #                     "simpleText": {
    #                         "text": menu
    #                     }
    #                 }
    #             ]
    #         }
    #     )
    #         return response_body
		

@app.post("/tommorowMenu", response_model=None)
def fetch_tommorow_menu(content: dict,db:Session = Depends(get_db)):
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.get_user_by_user_id(db,user_id=user_id)
    if (user.dormitory =="세종"):
        response_body = ResponseBody(
        version="2.0",
        template={
            "outputs": [
                {
                    "simpleText": {
                        "text": meal.tommorowMenu()
                    }
                }
            ]
        }
    )
    else:
        response_body = ResponseBody(
        version="2.0",
        template={
            "outputs": [
                {
                    "simpleText": {
                        "text": menu
                    }
                }
            ]
        }
    )
        return response_body
		


@app.post("/weekMenu", response_model=None)
def fetch_week_menu(content: dict,db:Session = Depends(get_db)):
    user_id = content['userRequest']['user']['properties']['plusfriend_user_key']
    user = crud.get_user_by_user_id(db,user_id=user_id)
    if (user.dormitory =="세종"):
        response_body = ResponseBody(
        version="2.0",
        template={
            "outputs": [
                {
                    "simpleText": {
                        "text": meal.weekMenu(content)
                    }
                }
            ]
        }
    )
    else:
        response_body = ResponseBody(
        version="2.0",
        template={
            "outputs": [
                {
                    "simpleText": {
                        "text": menu
                    }
                }
            ]
        }
    )
        return response_body
		


@app.post("/complete")
def register_alarm(response: Dict, db:Session = Depends(get_db)):
    user_id = response['userRequest']['user']['properties']['plusfriend_user_key']
    #user_id 가 이미 있는지 검사
    user = get_user_by_user_id(db,user_id=user_id)
    있으면 
    if user:
        return KakaoTemplate.simple_text("이미 등록된 사용자입니다.")
    
    else:
        
    	dormitory=response['action']['clientExtra']['Dormitory_item']
    	create = create_user(db = db, user_id=user_id, dormitory=dormitory)

    return {
    	"version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": dormitory +"기숙사로 등록되었습니다."
                    }
                }
            ],
            "quickReplies" : [
                {
                    "messageText": "오늘 식단",
                    "action": "message",
                    "label": "오늘 식단"
                },
                {
                    "messageText": "내일 식단",
                    "action": "message",
                    "label": "내일 식단"
     			 },
                {
                    "messageText": "주간 식단",
                    "action": "message",
                    "label": "주간 식단"
      			},
            ]
        }
    }  
    
@app.post("/updateDormitory")
def update_dormitory(response: Dict, db:Session = Depends(get_db)):
    print(response)
    user_id = response['userRequest']['user']['properties']['plusfriend_user_key']
    dormitory=response['action']['clientExtra']['Dormitory_item']
    user = crud.get_user_by_user_id(db,user_id=user_id)
    
    if(user.dormitory!=dormitory):
        user.dormitory=dormitory
        db.commit()
    return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": user.dormitory + "기숙사로 수정되었습니다."
                }
            }
        ],
        "quickReplies" : [
                {
                    "messageText": "오늘 식단",
                    "action": "message",
                    "label": "오늘 식단"
                },
                {
                    "messageText": "내일 식단",
                    "action": "message",
                    "label": "내일 식단"
     			 },
                {
                    "messageText": "주간 식단",
                    "action": "message",
                    "label": "주간 식단"
      			},
            ]
    }
}   
    
@app.post("/items/")
def create_item(response: Dict):
    payload =  response    
    print(payload)
    return payload
    
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=2000)
    
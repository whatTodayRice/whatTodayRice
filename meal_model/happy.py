from datetime import datetime, timezone, timedelta
from sql_app import crud
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal,engine
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import locale

locale.setlocale(locale.LC_TIME, 'ko_KR.utf-8')

'''
오늘, 내일, 주간메뉴를 받아오는 코드
'''

class Happy:
    def fetch_today_menu(self, db:Session):
        KST = timezone(timedelta(hours=9))
        date = datetime.now(KST).strftime("%Y-%m-%d")
        date_of_selected_menu = datetime.now(KST).strftime('%m/%d(%a)')
        
        menu_item = crud.read_happy_menu(db=db, date=date)
        
        breakfast=menu_item.breakfast
        takeout =menu_item.takeout
        lunch=menu_item.lunch
        dinner=menu_item.dinner

        menu= f'😊 {date_of_selected_menu} 식단입니다.\n\n🍙조식🍙\n{breakfast}\n\nTAKE-OUT : {takeout}\n\n🍘중식🍘\n{lunch}\n\n🍱석식🍱\n{dinner}'
        return menu
    
    def fetch_tomorrow_menu(self, db:Session):
        
        KST = timezone(timedelta(hours=9))
        time_record = datetime.now(KST) + timedelta(days=1)
        date = time_record.strftime("%Y-%m-%d")
        date_of_selected_menu = time_record.strftime('%m/%d(%a)')

        menu_item = crud.read_happy_menu(db=db, date=date)
        
        breakfast=menu_item.breakfast
        takeout =menu_item.takeout
        lunch=menu_item.lunch
        dinner=menu_item.dinner

        menu= f'😊 {date_of_selected_menu} 식단입니다.\n\n🍙조식🍙\n{breakfast}\n\nTAKE-OUT : {takeout}\n\n🍘중식🍘\n{lunch}\n\n🍱석식🍱\n{dinner}'
        return menu
    
    def fetch_week_menu(self,  db:Session,content:dict):
        user_date =content['action']['clientExtra']['week_day']
        weekday_map = {
            "월": MO,
            "화": TU,
            "수": WE,
            "목": TH,
            "금": FR,
            "토": SA,
            "일": SU,
        }
        selected_day = weekday_map[user_date]

        KST = timezone(timedelta(hours=9))
        today = datetime.now(KST).date()
        days_since_monday = today.weekday()  
        monday_of_week = today - timedelta(days=days_since_monday)
        selected_date = monday_of_week + relativedelta(weekday=selected_day)
        user_selected_date = selected_date.strftime('%Y-%m-%d')
        date_of_selected_menu = selected_date.strftime('%m/%d(%a)')

        menu_item = crud.read_happy_menu(db=db, date=user_selected_date)
        
        breakfast=menu_item.breakfast
        takeout =menu_item.takeout
        lunch=menu_item.lunch
        dinner=menu_item.dinner
        
        menu= f'😊 {date_of_selected_menu} 식단입니다.\n\n🍙조식🍙\n{breakfast}\n\nTAKE-OUT : {takeout}\n\n🍘중식🍘\n{lunch}\n\n🍱석식🍱\n{dinner}'
        return menu


         
   
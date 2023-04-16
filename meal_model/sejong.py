from datetime import datetime, timezone, timedelta
from sql_app import crud
from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import locale
from constants import Constants

locale.setlocale(locale.LC_TIME, 'ko_KR.utf-8')

'''
	오늘, 내일, 주간메뉴를 받아오는 코드
'''

class Sejong:
    def fetch_today_menu(self, db:Session):
        KST = timezone(timedelta(hours=9))
        date = datetime.now(KST).strftime("%Y-%m-%d")    
        date_of_selected_menu = datetime.now(KST).strftime('%m/%d(%a)')

        menu_item = crud.read_sejong_menu(db=db, date=date)
        db_breakfast=menu_item.breakfast
        breakfast= ', '.join(db_breakfast.split('\n'))
        db_lunch=menu_item.lunch
        lunch = ', '.join(db_lunch.split('\n'))
        db_dinner=menu_item.dinner
        dinner = ', '.join(db_dinner.split('\n'))
        
        menu= f'😊 {date_of_selected_menu} 식단입니다.\n\n🍙아침🍙\n{breakfast}\n\n🍘점심🍘\n{lunch}\n\n🍱저녁🍱\n{dinner}'
        return menu
    
    def fetch_tomorrow_menu(self, db:Session):
        KST = timezone(timedelta(hours=9))
        time_record = datetime.now(KST) + timedelta(days=1)
        date = time_record.strftime("%Y-%m-%d")    
        date_of_selected_menu = time_record.strftime('%m/%d(%a)')

        menu_item = crud.read_sejong_menu(db=db, date=date)
        
        db_breakfast=menu_item.breakfast
        breakfast= ', '.join(db_breakfast.split('\n'))
        db_lunch=menu_item.lunch
        lunch = ', '.join(db_lunch.split('\n'))
        db_dinner=menu_item.dinner
        dinner = ', '.join(db_dinner.split('\n'))
        
        menu_text= f'😊 {date_of_selected_menu} 식단입니다.\n\n🍙아침🍙\n{breakfast}\n\n🍘점심🍘\n{lunch}\n\n🍱저녁🍱\n{dinner}'
        announcement_text = f'\n\n{Constants.sejong_weekday_restaurant_hours_text}\n\n{Constants.for_notification_text}'
        menu = menu_text + announcement_text
        return menu
    
    def fetch_week_menu(self, db:Session, content:dict):
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

        # Calculate the date of the selected day for the current week
        KST = timezone(timedelta(hours=9))
        today = datetime.now(KST).date()
        days_since_monday = today.weekday()  # Monday is 0 and Sunday is 6
        monday_of_week = today - timedelta(days=days_since_monday)
        selected_date = monday_of_week + relativedelta(weekday=selected_day)
        user_selected_date = selected_date.strftime('%Y-%m-%d')
        date_of_selected_menu = selected_date.strftime('%m/%d(%a)')
        
        menu_item = crud.read_sejong_menu(db=db, date=user_selected_date)
        
        db_breakfast=menu_item.breakfast
        breakfast= ', '.join(db_breakfast.split('\n'))
        db_lunch=menu_item.lunch
        lunch = ', '.join(db_lunch.split('\n'))
        db_dinner=menu_item.dinner
        dinner = ', '.join(db_dinner.split('\n'))
        
        menu= f'😊 {date_of_selected_menu} 식단입니다.\n\n🍙아침🍙\n{breakfast}\n\n🍘점심🍘\n{lunch}\n\n🍱저녁🍱\n{dinner}'
        return menu
    

       

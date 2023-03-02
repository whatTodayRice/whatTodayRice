from datetime import datetime, timezone, timedelta
from sql_app import crud
from sqlalchemy.orm import Session


'''
	오늘, 내일, 주간메뉴를 받아오는 코드
'''

class Sejong:
    def fetch_today_menu(self, db:Session):
        KST = timezone(timedelta(hours=9))
        date = datetime.now(KST).strftime("%Y-%m-%d")             
        menu_item = crud.read_sejong_menu(db=db, date=date)
        db_breakfast=menu_item.breakfast
        breakfast= ', '.join(db_breakfast.split('\n'))
        db_lunch=menu_item.lunch
        lunch = ', '.join(db_lunch.split('\n'))
        db_dinner=menu_item.dinner
        dinner = ', '.join(db_dinner.split('\n'))
        menu = f'🍙아침🍙\n{breakfast}\n\n🍘점심🍘\n{lunch}\n\n🍱저녁🍱\n{dinner}'
        return menu
    
    def fetch_tomorrow_menu(self, db:Session):
        KST = timezone(timedelta(hours=9))
        time_record = datetime.now(KST) + timedelta(days=1)
        date = time_record.strftime("%Y-%m-%d")         
        menu_item = crud.read_sejong_menu(db=db, date=date)
        
        db_breakfast=menu_item.breakfast
        breakfast= ', '.join(db_breakfast.split('\n'))
        db_lunch=menu_item.lunch
        lunch = ', '.join(db_lunch.split('\n'))
        db_dinner=menu_item.dinner
        dinner = ', '.join(db_dinner.split('\n'))
        
        menu = f'🍙아침🍙\n{breakfast}\n\n🍘점심🍘\n{lunch}\n\n🍱저녁🍱\n{dinner}'
        return menu
    
    def fetch_week_menu(self, db:Session, content:dict):
        date = content["action"]["detailParams"]["date"]["origin"]
        menu_item = crud.read_sejong_menu(db=db, date=date)
        
        db_breakfast=menu_item.breakfast
        breakfast= ', '.join(db_breakfast.split('\n'))
        db_lunch=menu_item.lunch
        lunch = ', '.join(db_lunch.split('\n'))
        db_dinner=menu_item.dinner
        dinner = ', '.join(db_dinner.split('\n'))
        
        menu= f'🍙아침🍙\n{breakfast}\n\n🍘점심🍘\n{lunch}\n\n🍱저녁🍱\n{dinner}'
        return menu

from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
import ssl
from typing import Dict
from test_selenium import CheckMenu



class MealModel:
    def todayMenu(self):
        
        week_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        response = "https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php"
        context = ssl._create_unverified_context()
        html = urlopen(response,context=context).read()
        soup = BeautifulSoup(html, 'html.parser')
        td_tags_breakfast = soup.select("td:contains('아침')~td")
        td_tags_lunch = soup.select("td:contains('점심')~td")
        td_tags_dinner = soup.select("td:contains('저녁')~td")
        td_tags = soup.select("th:contains('요일')~th")
    
        for i in range(0, 7):
            KST = timezone(timedelta(hours=9))
            time_record = datetime.now(KST)
            if time_record.strftime("%A") == week_list[i]:
                breakfast = td_tags_breakfast[i].text
                lunch = td_tags_lunch[i].text
                dinner = td_tags_dinner[i].text
                
        breakfast = breakfast.strip().replace("\r\n", ",")
        lunch = lunch.strip().replace("\r\n", ",")
        dinner = dinner.strip().replace("\r\n", ",")
        
        if CheckMenu.isCheckMenu():
            print("죄송합니다 ㅠㅠㅠㅠ 식단이 늦어지고 있어요.")
        else:
            menu = f'아침\n{breakfast}\n\n점심\n{lunch}\n\n저녁\n{dinner}'
        return menu
    
    def tomorrowMenu(self):
        
        week_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        response = "https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php"
        context = ssl._create_unverified_context()
        html = urlopen(response,context=context).read()
        soup = BeautifulSoup(html, 'html.parser')
        td_tags_breakfast = soup.select("td:contains('아침')~td")
        td_tags_lunch = soup.select("td:contains('점심')~td")
        td_tags_dinner = soup.select("td:contains('저녁')~td")
        td_tags = soup.select("th:contains('요일')~th")
        for i in range(0, 7):
            week_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            KST = timezone(timedelta(hours=9))
            time_record = datetime.now(KST)- timedelta(days=1)
            if time_record.strftime("%A") == week_list[i]:
                breakfast = td_tags_breakfast[i].text
                lunch = td_tags_lunch[i].text
                dinner = td_tags_dinner[i].text
                
        breakfast = breakfast.strip().replace("\r\n", ",")
        lunch = lunch.strip().replace("\r\n", ",")
        dinner = dinner.strip().replace("\r\n", ",")
        
        
        menu = f'아침\n{breakfast}\n\n점심\n{lunch}\n\n저녁\n{dinner}'
        return menu
        
    def selectWeekMeal(self,content:dict):
        date = datetime.strptime(content["action"]["detailParams"]["date"]["origin"], '%Y-%m-%d').date()
        print(date)
        day_of_week = date.strftime("%A")

        week_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        response = "https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php"
        context = ssl._create_unverified_context()

        html = urlopen(response,context=context).read()
        soup = BeautifulSoup(html, 'html.parser')
        td_tags_breakfast = soup.select("td:contains('아침')~td")
        td_tags_lunch = soup.select("td:contains('점심')~td")
        td_tags_dinner = soup.select("td:contains('저녁')~td")
        td_tags = soup.select("th:contains('요일')~th")

        for i in range(0, 7):
            if day_of_week == week_list[i]:
                breakfast = td_tags_breakfast[i].text
                lunch = td_tags_lunch[i].text
                dinner = td_tags_dinner[i].text
                 
        breakfast = breakfast.strip().replace("\r\n", ",")
        lunch = lunch.strip().replace("\r\n", ",")
        dinner = dinner.strip().replace("\r\n", ",")
        
        
        menu = f'아침\n{breakfast}\n\n점심\n{lunch}\n\n저녁\n{dinner}'
        return menu
    

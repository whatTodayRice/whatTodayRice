from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime , timezone, timedelta
from sql_app import crud
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine

'''
	세종 토요일 식단 스크랩 및 DB 저장 코드
'''
class SejongSatMenu:
    def scrap_save_Sat_menu():
        options = Options()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')

        driver = webdriver.Chrome(options=options)
        url = "https://dormitory.pknu.ac.kr/03_notice/notice01.php"
        driver.get(url)
        db = SessionLocal()
        
        breakfast_x_path = '//*[@id="calField"]/div/table/tbody/tr[1]/td[8]'
        lunch_x_path = '//*[@id="calField"]/div/table/tbody/tr[2]/td[8]'
        dinner_x_path = '//*[@id="calField"]/div/table/tbody/tr[3]/td[8]'
        
        date_string = driver.find_element_by_xpath('//*[@id="calField"]/div/table/thead/tr/th[8]').text
        print(date_string)
        date_obj = date_string.split("(")[1].rstrip(")")
        date = datetime.strptime(date_obj, "%m/%d")
        iso_date_str = date.replace(year=2023).strftime("%Y-%m-%d")

        breakfast = driver.find_element_by_xpath(breakfast_x_path).text
        lunch = driver.find_element_by_xpath(lunch_x_path).text
        dinner = driver.find_element_by_xpath(dinner_x_path).text
        crud.save_sejong_menu(db=db, date=iso_date_str, breakfast = breakfast,lunch = lunch , dinner = dinner)

        db.close()
        driver.quit()
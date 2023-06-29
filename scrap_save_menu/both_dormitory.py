from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from typing import Dict
from selenium.webdriver.common.by import By
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sql_app import crud
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal,engine
import time


class ScrapAndSave:
    
    '''
    	세종 일 ~ 금 식단 스크랩 및 DB 저장 코드
    '''

    def sejong_scrap_save_menu():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        url = "https://dormitory.pknu.ac.kr/03_notice/notice01.php"
        driver.get(url)
        db = SessionLocal()
        next_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="calField"]/p/a[2]/img')))
        next_button.click()
        time.sleep(5)

        for i in range(2,8):
            date_x_path = f'//*[@id="calField"]/div/table/thead/tr/th[{i}]'
            breakfast_x_path = f'//*[@id="calField"]/div/table/tbody/tr[1]/td[{i}]'
            lunch_x_path= f'//*[@id="calField"]/div/table/tbody/tr[2]/td[{i}]'
            dinner_x_path = f'//*[@id="calField"]/div/table/tbody/tr[3]/td[{i}]'

            date_string = driver.find_element_by_xpath(date_x_path).text
            date_obj = date_string.split("(")[1].rstrip(")")
            date = datetime.strptime(date_obj, "%m/%d")
            iso_date_str = date.replace(year=2023).strftime("%Y-%m-%d")           

            breakfast = driver.find_element_by_xpath(breakfast_x_path).text
            lunch =driver.find_element_by_xpath(lunch_x_path).text
            dinner = driver.find_element_by_xpath(dinner_x_path).text
            crud.save_sejong_menu(db=db, date=iso_date_str,breakfast=breakfast,lunch=lunch , dinner=dinner)

        db.close()
        driver.close()
    
    '''
    행복 식단 스크랩 및 DB 저장 코드 
    '''

    def happy_scrap_save_menu():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        
        
        url = "https://happydorm.or.kr/busan/ko/0606/cafeteria/menu/"
    
        driver.get(url)
        db = SessionLocal()
        
        driver.find_element_by_xpath('//*[@id="sub"]/div/div/div[2]/a[2]').click()
        driver.find_element_by_xpath('//*[@id="showAllBtn"]').click()

        for i in range(2,9):
            date_x_path = f'//*[@id="sub"]/div/div/table[{i}]/thead/tr/th'
            breakfast_x_path = f'//*[@id="sub"]/div/div/table[{i}]/tbody/tr[1]/td[1]'
            takeout_x_path = f'//*[@id="sub"]/div/div/table[{i}]/tbody/tr[2]/td[1]'
            lunch_x_path= f'//*[@id="sub"]/div/div/table[{i}]/tbody/tr[3]/td[1]'
            dinner_x_path = f'//*[@id="sub"]/div/div/table[{i}]/tbody/tr[6]/td[1]'

            date_string = driver.find_element_by_xpath(date_x_path).text
            date = date_string.split(" ")[1].strip("()")

            breakfast = driver.find_element_by_xpath(breakfast_x_path).text
            takeout=driver.find_element_by_xpath(takeout_x_path).text
            lunch =driver.find_element_by_xpath(lunch_x_path).text
            dinner = driver.find_element_by_xpath(dinner_x_path).text
            crud.save_menu(db=db, date=date, breakfast=breakfast, takeout=takeout ,lunch=lunch , dinner=dinner)
            
        db.close()
        driver.quit()
    
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

'''
셀레니움을 이용하여 다음 주 식단이 있는지 확인하는 코드
'''

class CheckMenu:
    def isCheckMenu():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.get('https://dormitory.pknu.ac.kr/03_notice/notice01.php')
        driver.find_element(By.XPATH, r'//*[@id="calField"]/p/a[1]/img').click()
        time.sleep(1)

        menu = driver.find_element(By.XPATH, r'//*[@id="calField"]/div/table/tbody/tr[1]/td[2]').text

        if menu =="":
            return True
        driver.quit()
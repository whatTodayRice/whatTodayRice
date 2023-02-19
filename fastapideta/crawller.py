import requests
from bs4 import BeautifulSoup
from datetime import datetime

week_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

res = requests.get("https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php", verify=False)
html = res.text
soup = BeautifulSoup(html, 'html.parser')
td_tags_breakfast = soup.select("td:contains('아침')~td")
td_tags_lunch = soup.select("td:contains('점심')~td")
td_tags_dinner = soup.select("td:contains('저녁')~td")
td_tags = soup.select("th:contains('요일')~th")

for i in range(0, 7):
    if datetime.today().strftime("%A") == week_list[i]:
        breakfast = td_tags_breakfast[i].text
        lunch = td_tags_lunch[i].text
        dinner = td_tags_dinner[i].text

new_breakfast =breakfast.strip().replace("\r\n", ",")
menu = {
    "breakfast": breakfast.strip().replace("\r\n", ","),
    "lunch": lunch.strip().replace("\r\n", ","),
    "dinner": dinner.strip().replace("\r\n", ",")}

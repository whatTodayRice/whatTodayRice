import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
app = FastAPI()


@app.get("/meal_table")
def get_meal_table():

    res = requests.get("https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php",verify=False)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    td_tags = soup.select("td:contains('아침')")

    for td in td_tags:
        print(td.text)


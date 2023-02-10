from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
from datetime import datetime ,timezone,timedelta
from urllib.request import Request, urlopen
import ssl


app = FastAPI()


class ResponseBody(BaseModel):
    version: str
    template: dict


@app.get("/")
def read_root():
    return {"hello": 'World'}


@app.post("/showHello")
def show_hello():
    response_body = ResponseBody(
        version="2.0",
        template={
            "outputs": [
                {
                    "simpleText": {
                        "text": week()
                    }
                }
            ]
        }
    )

    return response_body

def week():
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
        time_record=datetime.now(KST)
        if time_record.strftime("%A") == week_list[i]:
            breakfast = td_tags_breakfast[i].text
            lunch = td_tags_lunch[i].text
            dinner = td_tags_dinner[i].text

    menu = {
        "breakfast": breakfast.strip().replace("\r\n", ","),
        "lunch": lunch.strip().replace("\r\n", ","),
        "dinner": dinner.strip().replace("\r\n", ",")}
    
    return str(menu)
    


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)

import requests
from bs4 import BeautifulSoup

url = "https://dormitory.pknu.ac.kr/03_notice/req_getSchedule.php"
response = requests.get(url,verify=False)
soup = BeautifulSoup(response.text, "html.parser")
td_tags = soup.select("td") #아침

for td in td_tags:
    print(td.text)
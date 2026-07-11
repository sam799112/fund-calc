import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def get_fund_data():
    nav_res = requests.get("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64", headers=headers)
    nav_soup = BeautifulSoup(nav_res.content, 'html.parser')
    nav = nav_soup.find(id="Nav").text.strip()

    div_res = requests.get("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64", headers=headers)
    div_soup = BeautifulSoup(div_res.content, 'html.parser')
    div = div_soup.find(class_="t3n0").text.strip()

    return {"nav": nav, "div": div, "date": datetime.now().strftime("%Y-%m-%d")}

with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)

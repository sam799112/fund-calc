import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_fund_data():
    # 抓取淨值頁面
    nav_res = requests.get("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64", headers=headers)
    nav_soup = BeautifulSoup(nav_res.content, 'html.parser')
    
    # 改用更寬鬆的搜尋方式：找所有含有淨值數值的 td
    # MoneyDJ 常見的淨值位在第一個 class 為 't3n0' 的 td 中
    nav_tag = nav_soup.select_one('td.t3n0')
    nav = nav_tag.text.strip() if nav_tag else "0.00"

    # 抓取配息頁面
    div_res = requests.get("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64", headers=headers)
    div_soup = BeautifulSoup(div_res.content, 'html.parser')
    
    # 同樣改用 select_one 找配息
    div_tag = div_soup.select_one('td.t3n0')
    div = div_tag.text.strip() if div_tag else "0.00"

    return {"nav": nav, "div": div, "date": datetime.now().strftime("%Y-%m-%d")}

with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_fund_data():
    # 抓取淨值
    nav_res = requests.get("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64", headers=headers)
    nav_soup = BeautifulSoup(nav_res.content, 'html.parser')
    # 找尋淨值：通常在 table 裡，我們要排除掉日期的欄位
    # 我們精確抓取 ID 為 Nav 的 span
    nav = nav_soup.find(id="Nav").text.strip() if nav_soup.find(id="Nav") else "0.00"

    # 抓取配息
    div_res = requests.get("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64", headers=headers)
    div_soup = BeautifulSoup(div_res.content, 'html.parser')
    # 找尋配息：配息表格中，數值通常在第二個 t3n0 類別的 td 中
    tags = div_soup.select('td.t3n0')
    # 如果找到了多個 td.t3n0，我們取第二個，通常那裡才是金額
    div = tags[1].text.strip() if len(tags) > 1 else (tags[0].text.strip() if tags else "0.00")

    return {"nav": nav, "div": div, "date": datetime.now().strftime("%Y-%m-%d")}

with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)

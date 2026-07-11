import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# 通用抓取函數
def get_data(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # 偵錯用：如果您抓不到數字，GitHub Logs 會印出它抓到的所有文字，方便您檢查
        all_td = soup.find_all('td')
        
        for td in all_td:
            text = td.text.strip()
            # 確保是數字格式 (簡單的正則匹配)
            if re.match(r'^\d+\.\d+$', text):
                return text
        
        # 如果走到這裡都沒回傳，代表沒抓到數字
        print(f"Debug: 網址 {url} 未找到數字")
        return "0.00"
    except Exception as e:
        print(f"Debug: 抓取 {url} 時發生錯誤: {e}")
        return "0.00"

def get_fund_data():
    # 1. 安聯收益成長 (DSP5)
    dsp5_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=TLZ64")
    dsp5_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=TLZ64")
    
    # 2. 摩根多重收益 (JFZN3)
    jpm_nav = get_data("https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=jfzn3")
    jpm_div = get_data("https://www.moneydj.com/funddj/yp/wb05.djhtm?a=JFZN3")

    # 3. 貝萊德世界科技 (MLE24)
    # 使用您提供的富邦官網連結
    mle24_url = "https://invest.fubonlife.com.tw/content.html?sUrl=$W$WB$WB05]DJHTM{A}SH^V9-MLE24"
    mle24_nav = get_data(mle24_url)
    mle24_div = mle24_nav # 若抓不到配息，之後可再調整為固定值或手動設定
    
    # 打包數據
    return {
        "nav": dsp5_nav, 
        "div": dsp5_div, 
        "jpm_nav": jpm_nav, 
        "jpm_div": jpm_div,
        "mle24_nav": mle24_nav,
        "mle24_div": mle24_div,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

# 將結果寫入 data.json
with open('data.json', 'w') as f:
    json.dump(get_fund_data(), f)

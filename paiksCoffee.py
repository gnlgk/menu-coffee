from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "paiks"
filename = f"{folder_path}/menupaiks_{current_date}.json"

# 폴더 생성
os.makedirs(folder_path, exist_ok=True)

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

try:
    browser.get("https://paikdabang.com/menu/menu_coffee/")

    # 페이지가 완전히 로드될 때까지 대기
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "menu_list"))
    )

    # 업데이트된 페이지 소스를 변수에 저장
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 데이터 추출
    coffee_data = []
    tracks = soup.select("#content-wrap > div.sub_section.menu_wrap > div > div.menu_list.clear > ul > li")

    for track in tracks:
        title = track.select_one("p").text.strip()
        image_url = track.select_one("div.thumb > img").get('src')
        titleE = track.select_one(".hover > .menu_tit2.color-1").text.strip()
        description = track.select_one(".hover > .txt").text.strip()

        nutrition_info = {}
        tbody = track.select_one(".ingredient_table")
        if tbody:
            rows = tbody.find_all("li")
            for row in rows:
                key_elem = row.select_one("div:nth-child(1)")
                value_elem = row.select_one("div:nth-child(2)")
                key = key_elem.text.strip() if key_elem else "Unknown"
                value = value_elem.text.strip() if value_elem else "Unknown"
                nutrition_info[key] = value

        coffee_data.append({
            "brand": "빽다방",
            "title": title,
            "titleE": titleE,
            "imageURL": image_url,
            "description": description,  # Fixed typo
            "information": nutrition_info,
            "address": "https://paikdabang.com/"
        })
finally:
    # 브라우저 종료
    browser.quit()

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

print(f"Data successfully saved to {filename}")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import json
import os
from urllib.parse import urljoin

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "gurunaru"
filename = f"{folder_path}/menugurunaru_{current_date}.json"

# 폴더 생성
os.makedirs(folder_path, exist_ok=True)

# 웹드라이버 설치
options = ChromeOptions()
options.add_argument("--headless")  # 실행 중 브라우저가 보이지 않도록 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

try:
    browser.get("https://www.coffine.co.kr/front/menu/coffee_list.php#contents")

    # 업데이트된 페이지 소스를 변수에 저장
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > div > div > .pro_list > li"))
    )
    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')

    # 데이터 추출
    coffee_data = []
    tracks = soup.select("#contents > div > div > .pro_list > li")

    for track in tracks:
        # 각 커피 항목의 링크(Anchor 태그)를 찾습니다.
        coffee_link = track.select_one("a").get('href')
        coffee_url = urljoin(browser.current_url, coffee_link)
        
        # 상세 페이지로 이동하여 추가 데이터를 가져옵니다.
        browser.get(coffee_url)
        
        # 페이지가 완전히 로드될 때까지 대기
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "menu_view_wrap"))
        )
        
        # 상세 페이지의 소스를 변수에 저장
        detail_page_source = browser.page_source
        detail_soup = BeautifulSoup(detail_page_source, 'html.parser')
        
        try:
            title = detail_soup.select_one(".menu_view_wrap > .menu_info > h3").text.strip()  
            titleE = detail_soup.select_one(".menu_view_wrap > .menu_info > .name_eng").text.strip()  
            image_url = detail_soup.select_one(".menu_view_wrap > .menu_image > img.img").get('src').replace('/uploads', 'https://www.coffine.co.kr/uploads')
            description = detail_soup.select_one(".menu_view_wrap > .menu_info > .txt").text.strip() 
            
            coffee_data.append({
                "brand": "커핀그루나루",
                "title": title,
                "titleE": titleE,
                "imageURL": image_url,
                "description": description,
                "address": "https://www.coffine.co.kr/"
            })
        except AttributeError as e:
            print(f"Error processing {coffee_url}: {e}")
            continue

finally:
    # 브라우저 종료
    browser.quit()

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

print(f"Data has been saved to {filename}")


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

# 현재 날짜 가져오기
current_date = datetime.now().strftime("%Y-%m-%d")
folder_path = "bombom"
filename = f"{folder_path}/menubombom_{current_date}.json"

# 웹드라이브 설치
options = ChromeOptions()
service = ChromeService(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)

# 첫 번째 페이지로 이동
browser.get("http://www.cafebombom.co.kr/bbs/board.php?bo_table=menu&sca=COFFEE&page=1")
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "gall_ul")))

# 커피 정보를 저장할 리스트
coffee_data = []

# 현재 페이지의 커피 정보 가져오기
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')
tracks = soup.select("#gall_ul > li > div > .gall_con > .gall_img > span")
for track in tracks:
    coffee_link = track.select_one("a").get('href')
    browser.get(f"{coffee_link}")
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "bo_v_con")))
    detail_page_source = browser.page_source
    detail_soup = BeautifulSoup(detail_page_source, 'html.parser')
    title = detail_soup.select_one("#bo_v_con > div > .txt_box > h2").text.strip()
    titleE = detail_soup.select_one("#bo_v_con > div > .txt_box > p:nth-child(3)").text.strip()
    image_url = detail_soup.select_one("#bo_v_img > a > img").get('src')
    desction = detail_soup.select_one("#bo_v_con > div > .txt_box > p:nth-child(4)").text.strip()
    coffee_data.append({
        "brand": "봄봄",
        "title": title,
        "titleE": titleE,
        "imageURL": image_url,
        "desction": desction,
        "address": "http://www.cafebombom.co.kr"
    })
    # print(f"Added coffee data: {coffee_data[-1]}")

# 두 번째 페이지로 이동
browser.get("http://www.cafebombom.co.kr/bbs/board.php?bo_table=menu&sca=COFFEE&page=2")
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "gall_ul")))

# 현재 페이지의 커피 정보 가져오기
html_source_updated = browser.page_source
soup = BeautifulSoup(html_source_updated, 'html.parser')
tracks = soup.select("#gall_ul > li > div > .gall_con > .gall_img > span")
for track in tracks:
    coffee_link = track.select_one("a").get('href')
    browser.get(f"{coffee_link}")
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "bo_v_con")))
    detail_page_source = browser.page_source
    detail_soup = BeautifulSoup(detail_page_source, 'html.parser')
    title = detail_soup.select_one("#bo_v_con > div > .txt_box > h2").text.strip()
    titleE = detail_soup.select_one("#bo_v_con > div > .txt_box > p:nth-child(3)").text.strip()
    image_url = detail_soup.select_one("#bo_v_img > a > img").get('src')
    desction = detail_soup.select_one("#bo_v_con > div > .txt_box > p:nth-child(4)").text.strip()
    coffee_data.append({
        "brand": "봄봄",
        "title": title,
        "titleE": titleE,
        "imageURL": image_url,
        "desction": desction,
        "address": "http://www.cafebombom.co.kr"
    })
    # print(f"Added coffee data: {coffee_data[-1]}")

# 데이터를 JSON 파일로 저장
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(coffee_data, f, ensure_ascii=False, indent=4)

# 브라우저 종료
browser.quit()

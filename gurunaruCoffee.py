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

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def save_data_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def setup_browser():
    options = ChromeOptions()
    service = ChromeService(executable_path=ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def fetch_page_source(browser, url):
    browser.get(url)
    return browser.page_source

def wait_for_element(browser, by, value, timeout=20):
    WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, value)))

def extract_coffee_data(detail_soup):
    title = detail_soup.select_one(".menu_view_wrap > .menu_info > h3").text.strip()
    titleE = detail_soup.select_one(".menu_view_wrap > .menu_info > .name_eng").text.strip()
    image_url = detail_soup.select_one(".menu_view_wrap > .menu_image > img.img").get('src').replace('/uploads', 'https://www.coffine.co.kr/uploads')
    desction = detail_soup.select_one(".menu_view_wrap > .menu_info > .txt").text.strip()
    return {
        "brand": "커핀그루나루",
        "title": title,
        "titleE": titleE,
        "imageURL": image_url,
        "desction": desction,
        "address": "https://www.coffine.co.kr/"
    }

def main():
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = "gurunaru"
    filename = f"{folder_path}/menugurunaru_{current_date}.json"

    create_folder(folder_path)

    browser = setup_browser()

    try:
        main_url = "https://www.coffine.co.kr/front/menu/coffee_list.php#contents"
        browser.get(main_url)
        html_source_updated = browser.page_source
        soup = BeautifulSoup(html_source_updated, 'html.parser')

        coffee_data = []
        tracks = soup.select("#contents > div > div > .pro_list > li")

        for track in tracks:
            coffee_link = track.select_one("a").get('href')
            detail_url = f"https://www.coffine.co.kr/front/menu/{coffee_link}"
            browser.get(detail_url)
            wait_for_element(browser, By.CLASS_NAME, "menu_view_wrap")
            detail_page_source = browser.page_source
            detail_soup = BeautifulSoup(detail_page_source, 'html.parser')
            coffee_info = extract_coffee_data(detail_soup)
            coffee_data.append(coffee_info)
            time.sleep(2)  # Avoid overwhelming the server

        save_data_to_json(coffee_data, filename)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        browser.quit()

if __name__ == "__main__":
    main()

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
import re

# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to initialize and configure the Chrome WebDriver
def initialize_browser():
    options = ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Function to extract coffee data from the webpage
def extract_coffee_data(soup, page_title):
    coffee_data = []
    tracks = soup.select("#sub_con > div > div > .list_con > div > .list_con > ul > li")

    for track in tracks:
        title = track.select_one(".list_div .title_con .kor_con span").text.strip()
        en_title = track.select_one(".list_div .title_con .eng_con span").text.strip()
        image_style = track.select_one(".list_div .img_con").get('style')
        
        # Extract URL without surrounding quotes
        image_url_match = re.search(r'url\(["\']?(.*?)["\']?\)', image_style)
        if image_url_match:
            image_url = image_url_match.group(1).replace("/upload", "https://www.coffeebay.com/upload")
        else:
            image_url = "No Image URL"
        
        sub_title = track.select_one(".over_con > .contents_con.w_niceScroll_con > .contents_con.m_niceScroll_con > .info01_con > .intro_con span").text.strip()
        # content = track.select_one(".over_con > .contents_con.w_niceScroll_con > .contents_con.m_niceScroll_con > .info02_con > .info_con span").text.strip()

        canonical_link = soup.find('link', rel='canonical')
        address = canonical_link['href'].strip() if canonical_link else "No Address"

        coffee_data.append({
            "brand": page_title,
            "title": title,
            "titleE": en_title,
            "imageURL": image_url,
            "description": sub_title,
            # "information": content,
            "address": address
        })

    return coffee_data

# Main script execution
if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = "coffeebay"
    filename = f"{folder_path}/menucoffeebay_{current_date}.json"

    create_folder_if_not_exists(folder_path)
    browser = initialize_browser()
    browser.get("https://www.coffeebay.com/product/prd_menu.php?code=001&idx2=001")

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "list_con"))
    )

    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')
    page_title = soup.head.title.text.strip() if soup.head.title else "No Title"

    coffee_data = extract_coffee_data(soup, page_title)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(coffee_data, f, ensure_ascii=False, indent=4)

    browser.quit()

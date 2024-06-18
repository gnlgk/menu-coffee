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

# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to initialize and configure the Chrome WebDriver
def initialize_browser():
    options = ChromeOptions()
    options.add_argument("--headless")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Function to extract coffee data from a single page
def extract_coffee_data_from_page(browser, page_url, coffee_data):
    browser.get(page_url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "gall_ul")))

    html_source_updated = browser.page_source
    soup = BeautifulSoup(html_source_updated, 'html.parser')
    tracks = soup.select("#gall_ul > li > div > .gall_con > .gall_img > span")
    
    for track in tracks:
        coffee_link = track.select_one("a").get('href')
        browser.get(coffee_link)
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "bo_v_con")))
        
        detail_page_source = browser.page_source
        detail_soup = BeautifulSoup(detail_page_source, 'html.parser')
        title = detail_soup.select_one("#bo_v_con > div > .txt_box > h2").text.strip()
        titleE = detail_soup.select_one("#bo_v_con > div > .txt_box > p:nth-child(3)").text.strip()
        image_url = detail_soup.select_one("#bo_v_img > a > img").get('src')
        description = detail_soup.select_one("#bo_v_con > div > .txt_box > p:nth-child(4)").text.strip()
        
        coffee_data.append({
            "brand": "봄봄",
            "title": title,
            "titleE": titleE,
            "imageURL": image_url,
            "description": description,
            "address": "http://www.cafebombom.co.kr"
        })

# Main script execution
if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = "bombom"
    filename = f"{folder_path}/menubombom_{current_date}.json"

    create_folder_if_not_exists(folder_path)
    browser = initialize_browser()

    coffee_data = []
    base_url = "http://www.cafebombom.co.kr/bbs/board.php?bo_table=menu&sca=COFFEE&page="

    # Iterate through multiple pages
    for page_num in range(1, 3):  # Adjust the range as needed to cover more pages
        page_url = f"{base_url}{page_num}"
        extract_coffee_data_from_page(browser, page_url, coffee_data)

    # Save the data to a JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(coffee_data, f, ensure_ascii=False, indent=4)

    browser.quit()

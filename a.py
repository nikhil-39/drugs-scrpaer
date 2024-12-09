from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import urllib3
import os
import requests

def createCSV(drugs):
    df = pd.DataFrame(drugs, columns=['Name'])
    df_cleaned = df.dropna()
    final_df = df_cleaned.drop_duplicates()
    # final_df = final_df.reset_index()
    file_name = 'output_' + "migraine" + '.csv'
    final_df.to_csv(file_name, sep='\t', encoding='utf-8', index = False)

def extract(driver):
    data_list = []
    temp_html = driver.page_source
    temp_soup = BeautifulSoup(temp_html, "html.parser")
    name = temp_soup.find_all('div', class_="table-content")
    for i in name:
        data_list.append(i.text)
    
    return data_list

def initiate():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    urllib3.disable_warnings()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()


    url = "https://www.webmd.com/drugs/2/condition-1116/migraine"
    driver.get(url)
    return driver



driver = initiate()
drugs = extract(driver)
createCSV(drugs)


for drug in drugs:
    print(drug)

time.sleep(100)












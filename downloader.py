import requests
from bs4 import BeautifulSoup
import re
import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_soup(url):
    return BeautifulSoup(requests.get(url).text, features='lxml')
    
    
def get_chrome_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-popup-blocking')
    driver_exe = str(Path.home()/Path('webdrivers', 'chromedriver'))
    driver = webdriver.Chrome(driver_exe, options=chrome_options)
    return driver


def download_file(url, name):
    r = requests.get(url, stream=True)
    with open(name, 'wb') as f:
        for byte_chunk in r.iter_content(chunk_size=4096):
            f.write(byte_chunk)


def download_list_files(urls, names):
    i = 0
    while i < len(urls):
        print(f'Downloading {urls[i]} ==> {names[i]}')
        print(f'[{i + 1}/{len(urls)}]')
        try:
            download_file(urls[i], names[i])
        except:
            print(f'Error on {urls[i]} ==> {names[i]}')
            log_file = open('log', 'a')
            log_file.write(f'{urls[i]} ==> {names[i]}\n')
            log_file.close()
            i = i-1
            time.sleep(10)
        i = i+1

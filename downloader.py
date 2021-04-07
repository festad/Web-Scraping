import requests
from bs4 import BeautifulSoup
import re
import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def raw_to_normalized_string(string, pattern=re.compile(r'([0-9a-zA-Z]+)')):
    return '-'.join(chunk for chunk in pattern.findall(string)).lower()


def get_soup(url):
    return BeautifulSoup(requests.get(url).text, features='lxml')


def get_soup_with_random_session(url):
    session = requests.Session()
    return BeautifulSoup(session.get(url).text, 'lxml')
	
	
def create_and_move_into_dir(name):
    if name not in os.listdir():
        os.makedirs(name)
        os.chdir(name)
	

def path_check_in_home_and_move(name):
    os.chdir(Path.home())
    _create_and_move_into_dir(name)
    
    
def get_chrome_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-popup-blocking')
    driver_exe = str(Path.home()/Path('webdrivers', 'chromedriver'))
    driver = webdriver.Chrome(driver_exe, options=chrome_options)
    return driver


def get_firefox_driver(headless=False):
	firefox_options = webdriver.FirefoxOptions()
	if headless:
		firefox_options.add_argument('--headless')
	driver_exe = str(Path.home()/Path('webdrivers', 'geckodriver'))
	driver = webdriver.Firefox(options=firefox_options)
	return driver


def download_file(url, name):
    r = requests.get(url, stream=True)
    # extension = url.split('.')[-1]
    with open(f'{name}', 'wb') as f:
        for byte_chunk in r.iter_content(chunk_size=4096):
            f.write(byte_chunk)


def download_list_files(urls, names):
    i = 0
    while i < len(urls):
        print(f'Downloading {urls[i]} ==> {names[i]}')
        print(f'[{i + 1}/{len(urls)}]')
        download_file(urls[i], names[i])
        i = i+1
        #try:
            #download_file(urls[i], names[i])
        #except:
            #print(f'Error on {urls[i]} ==> {names[i]}')
            #log_file = open('log', 'a')
            #log_file.write(f'{urls[i]} ==> {names[i]}\n')
            #log_file.close()
            #i = i-1
            #time.sleep(10)
        #i = i+1
        
        
def normalize_number(k, n):
    upper_bound = f'{n}'
    upper_bound_digits = len(upper_bound)
    k_str = f'{k}'
    k_digits = len(k_str)
    return '0'*(upper_bound_digits - k_digits + 1) + k_str
        
        
def download_image(link, prefix, n):
    r = requests.Session().get(link)
    n_str = f'{n}'
    if len(n_str) == 1:
        namefile = f'{prefix}-000{n}.jpg'
    elif len(n_str) == 2:
        namefile = f'{prefix}-00{n}.jpg'
    elif len(n_str) == 3:
        namefile = f'{prefix}-0{n}.jpg'
    with open(namefile, 'wb') as f:
        for byte_chunk in r.iter_content(chunk_size=4096):
            f.write(byte_chunk)

import re
import sys
import os
from pathlib import Path
from downloader import get_soup, download_list_files
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def path_check():
    os.chdir(Path.home())
    if 'N_Hentai' not in os.listdir():
        os.makedirs('N_Hentai')
    os.chdir('N_Hentai')
    


def download_hentai(code):
    soup = get_soup(f'https://nhentai.net/g/{code}/')
    divs = soup.find_all('div', attrs={'class': 'tag-container field-name'})
    for d in divs:
        if 'Pages' in d.text:
            pages = int(re.search('[0-9]+', d.text).group(0))
    pages_urls = []
    pages_names = []
    driver_exe = '/home/insert-your-own-path/webdrivers/chromedriver_linux64/chromedriver'
    driver = webdriver.Chrome(driver_exe)
    for page in range(pages):
        driver.get(f'https://nhentai.net/g/{code}/{page+1}/')
        img_tags = WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))
        for it in img_tags:
            if 'galleries' in it.get_attribute('src'):
                pages_urls.append(it.get_attribute('src'))
                pages_names.append(f'{code}-{page+1}.jpg')
    download_list_files(pages_urls, pages_names)
    
    
def download_list_hentai(codes):
    for code in codes:
        if f'hentai-{code}' in os.listdir():
            print(f'Hentai {code} already present!')
        else:
            os.makedirs(f'hentai-{code}')
            os.chdir(f'hentai-{code}')
            download_hentai(code)
            os.chdir('..')


if __name__ == '__main__':
    path_check()
    if len(sys.argv) < 2:
        print('Insert the hentai(s) code(s)')
        sys.exit()
    download_list_hentai(sys.argv[1:])

import re
import sys
import os
import time
from pathlib import Path
from downloader import get_soup, download_list_files
from selenium import webdriver


def path_check():
    os.chdir(Path.home())
    if 'Libgen' not in os.listdir():
        os.makedirs('Libgen')
    os.chdir('Libgen')


def download_manga(hashcode, name):
    url = f'http://libgen.lc/comics/seriestable.php?series_hash={hashcode}'
    soup = get_soup(url)
    urls = []
    names = []
    counter = 1
    for atag in soup.find_all('a'):
        if 'get.php' in atag['href']:
            urls.append(f"http://libgen.lc/comics/{atag['href']}")
            names.append(f'{name}-{counter}')
            counter += 1
    if f'{name}' not in os.listdir():
        os.makedirs(f'{name}')
    os.chdir(f'{name}')
    driver_exe = '/home/denizu/webdrivers/chromedriver_linux64/chromedriver'
    counter = 1
    for url in urls:
        driver = webdriver.Chrome(driver_exe)
        print(f'{url} ==> {counter}')
        driver.get(url)
        time.sleep(100)
        counter += 1
    # download_list_files(urls, names)
    os.chdir('..')


if __name__ == '__main__':
    path_check()
    if len(sys.argv) < 3:
        print('Insert the manga hashcode first and then the name as arguments')
        sys.exit()
    download_manga(sys.argv[1], sys.argv[2])

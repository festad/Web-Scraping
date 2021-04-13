import os
import sys
import time
from pathlib import Path

from selenium import webdriver

from downloader import get_soup


def path_check():
    os.chdir(Path.home())
    if 'Libgen' not in os.listdir():
        os.makedirs('Libgen')
    os.chdir('Libgen')


def download_manga(hashcode, name, t=10):
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
    if name not in os.listdir():
        os.makedirs(name)
    # os.chdir(f'{name}')
    driver_exe = str(Path.home() / Path('chromedriver_linux64', 'chromedriver'))
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'download.default_directory': str(Path.home() / Path('Libgen', name))})

    counter = 1
    for url in urls:
        driver = webdriver.Chrome(driver_exe, options=options)
        print(f'{url} ==> {counter}')
        driver.get(url)
        time.sleep(int(t))
        counter += 1
    # download_list_files(urls, names)
    os.chdir('..')


if __name__ == '__main__':
    path_check()
    if len(sys.argv) < 3:
        print('Insert the manga hashcode, the name and the expected number of seconds')
        print('    to download a single file as arguments')
        print('ex: 3ed9638c0b9e53ece2c4d651a73e504f highschool-dxd 100')
        sys.exit()
    if len(sys.argv) == 4:
        download_manga(sys.argv[1], sys.argv[2], sys.argv[3])

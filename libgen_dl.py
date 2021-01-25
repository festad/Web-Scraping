import re
import sys
import os
from pathlib import Path
from downloader import get_soup, download_list_files


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
            urls.append(f"http://booksdl.org/comics/{atag['href']}")
            names.append(f'{name}-{counter}')
            counter += 1
    if f'{name}' not in os.listdir():
        os.makedirs(f'{name}')
    os.chdir(f'{name}')
    download_list_files(urls, names)
    os.chdir('..')


if __name__ == '__main__':
    path_check()
    if len(sys.argv) < 3:
        print('Insert the manga hashcode first and then the name as arguments')
        os.exit()
    download_manga(sys.argv[1], sys.argv[2])

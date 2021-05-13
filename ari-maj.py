import re
import time

import requests
from bs4 import BeautifulSoup


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
            i = i - 1
            time.sleep(10)
        i = i + 1


def ariadna_leak_scraping():
    pattern = re.compile('Ari.*jpg')
    urls = []
    names = []
    url = 'http://scandalplanet.com/ariadna-majewska/'
    soup = BeautifulSoup(requests.get(url).text, features='lxml')
    gallery_1 = soup.find(attrs={'id': 'gallery-1'})
    for g in gallery_1.find_all('a'):
        urls.append(g['href'])
        names.append(pattern.search(g['href']).group(0))
    download_list_files(urls, names)


def ariadna_second_leak_scraping():
    urls = []
    names = []
    url = 'https://cyberdrop.me/a/EpROZWXp'
    soup = BeautifulSoup(requests.get(url).text, features='lxml')
    for g in soup.find_all(attrs={'class': 'image'}):
        urls.append(g['href'])
        names.append(g['title'])
    download_list_files(urls, names)


if __name__ == '__main__':
    ariadna_second_leak_scraping()

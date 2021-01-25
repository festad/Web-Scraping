import requests
from bs4 import BeautifulSoup
import re
import json
import time


def get_soup(url):
    return BeautifulSoup(requests.get(url).text, features='lxml')


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

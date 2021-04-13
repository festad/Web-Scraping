import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

pattern_title = re.compile(r'([0-9a-zA-Z]+)')


def _raw_to_normalized_string(string, pattern=pattern_title):
    return '-'.join(chunk for chunk in pattern.findall(string)).lower()


def _get_soup_with_random_session(url):
    session = requests.Session()
    return BeautifulSoup(session.get(url).text, 'lxml')


def _create_and_move_into_dir(name):
    if name not in os.listdir():
        os.makedirs(name)
    os.chdir(name)


def _path_check_in_home_and_move(name):
    os.chdir(Path.home())
    _create_and_move_into_dir(name)


def _print_all_titles(url):
    soup = _get_soup_with_random_session(url)
    illustrations = soup.find_all('div', attrs={'class': 'description'})
    k = 1
    for ill in illustrations:
        if k >= 16:
            addr = ill.findChild('h3').findChild('a')
            # print(_raw_to_normalized_string(addr.text))
            _locate_volume(head + addr['href'])
        k += 1


def _locate_volume(url):
    soup = _get_soup_with_random_session(url)
    raw_title = list(soup.find('div', attrs={'class': 'titrePage'}).findChild('h2').children)[2].get_text()
    print(raw_title)
    # raw_title = BeautifulSoup(int_tag.findCh('a'), 'lxml').find_next_sibiling().get_text()
    title = _raw_to_normalized_string(raw_title)
    print(f'{title}')
    _create_and_move_into_dir(title)
    _recursive_navigation(url, title)
    _path_check_in_home_and_move('Pokemon')


def _recursive_navigation(url, title, counter=0):
    soup = _get_soup_with_random_session(url)
    nb_images = soup.find_all('p', attrs={'class': 'Nb_images'})
    if len(nb_images) == 0:
        preimage_addrs = []
        for wrapt in soup.find_all('span', attrs={'class': 'wrap2'}):
            preimage_addrs.append(wrapt.findChild('a')['href'])
        print(f'N images: {len(preimage_addrs)}')

        for p in preimage_addrs:
            print(f'#{counter + 1} -> {p}')
            soup = _get_soup_with_random_session(head + p)
            img_url = soup.find('img')['src']
            _download_image(head + img_url, title, counter + 1)
            counter += 1

        next_tags = soup.find_all('span', attrs={'class': 'navPrevNext'})
        print(f'NavPrevNexts -> {len(next_tags)}')
        for t in next_tags:
            # ass = t.findChildren('a', attrs={'rel':'next'})
            # print(len(ass))
            a = t.findChild('a', attrs={'rel': 'next'})
            if a is not None:
                _recursive_navigation(head + a['href'], title, counter)
        print('End!')
        return counter
    else:
        k = 0
        for nbi in nb_images:
            print(f"NESTED! -> {head + nbi.parent.parent.h3.a['href']}")
            k = _recursive_navigation(head + nbi.parent.parent.h3.a['href'], title, k)


def _download_image(link, prefix, n):
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


_path_check_in_home_and_move('Pokemon')

head = 'https://jb2448.info/'
url = 'https://jb2448.info/index.php?/category/922'
_print_all_titles(head)
# _locate_volume(url)

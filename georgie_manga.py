from pathlib import Path

import requests
import requests_random_user_agent

from downloader import normalize_number, download_file_inside_path

headers = {'Referer': 'https://mangakakalot.com/'}

base_link = 'https://bu3.mkklcdnv6tempv3.com/mangakakalot/l1/lady_georgie/vol1_chapter_1/1.jpg'

georgie = {1: [1, 2, 3, 4, 5, 6, 7],
           2: [8, 9, 10, 11, 12, 13],
           3: [14, 15, 16, 17, 18, 19, 20,
               21, 22, 23, 24, 25, 26, 27, 28],
           4: [29, 30, 31, 32, 33, 34, 35, 36, 37],
           5: [38, 39, 40, 41, 42, 43, 44, 45]}


def get_page(num_volume, num_chapter, num_page):
    return f'https://bu3.mkklcdnv6tempv3.com/mangakakalot/l1/lady_georgie/vol{num_volume}_chapter_{num_chapter}/{num_page}.jpg '


def download_chapter(num_volume, num_chapter):
    path = Path.home() / 'Manga' / 'Georgie' / f'volume_{num_volume}' / f'chapter_{num_chapter}'
    try:
        Path.mkdir(path)
    except Exception as e:
        print(f'==> {e}')
    num_page = 1
    while True:
        try:
            link = get_page(num_volume, num_chapter, num_page)
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                print(f'Downloading {link}')
                download_file_inside_path(link, f'{normalize_number(num_page, 99)}.jpg',
                                          path, headers=headers)
                print('Done!')
            elif response.status_code == 404:
                print(f'==> NOT FOUND: -> {link}')
                return
            elif response.status_code == 403:
                print(f'==> PERMISSION DENIED: -> {link}')
            else:
                print(response.text)
        except Exception as e:
            print(e)
        finally:
            num_page += 1


def download_volume(num_volume):
    print(f'Downloading volume {num_volume}')
    path = Path.home() / 'Manga' / 'Georgie' / f'volume_{num_volume}'
    try:
        Path.mkdir(path)
    except Exception as e:
        print(f'==> {e}')
    for num_chapter in georgie[num_volume]:
        print(f'Downloading chapter {num_chapter}')
        download_chapter(num_volume, num_chapter)
        print('Done!')
    print('Done!')


def download_manga():
    path = Path.home() / 'Manga' / 'Georgie'
    try:
        Path.mkdir(path)
    except Exception as e:
        print(f'==> {e}')
    for num_volume in georgie.keys():
        download_volume(num_volume)


if __name__ == '__main__':
    download_manga()

import re
from pathlib import Path

from downloader import (get_soup_with_random_session,
                        download_file_inside_path)


def download_pokemon_picture(url, path):
    try:
        soup = get_soup_with_random_session(url)
        img = soup.find('a', attrs={'class': 'image'}).img
        img_src = f"https:{img['src']}"
        img_name = img['alt']
        print(f'Downloading {img_name}')
        download_file_inside_path(img_src, img_name, path)
    except:
        print(f'===> Error with {url}')


def dl_driver():
    print('driver')
    if Path.home() / 'Pokemon' not in Path.home().iterdir():
        Path.mkdir(Path.home() / 'Pokemon')
    download_pokemon_picture("https://bulbapedia.bulbagarden.net/wiki/Omanyte_(Pok%C3%A9mon)", Path.home() / 'Pokemon')


def download_region(url):
    try:
        soup = get_soup_with_random_session(url)
        region = soup.find('h1', attrs={'id': 'firstHeading', 'class': 'firstHeading'}).text
        p = re.compile(r'Category:')
        region = p.sub('', region)
        p = re.compile(r'\W+')
        region = p.sub('_', region)
        if Path.home() / 'Pokemon' / f'{region}' not in Path(Path.home() / 'Pokemon').iterdir():
            Path.mkdir(Path.home() / 'Pokemon' / f'{region}')
        path = Path.home() / 'Pokemon' / f'{region}'
        cat = soup.find('div', attrs={'class': 'mw-category'})
        head = 'https://bulbapedia.bulbagarden.net'
        ps = cat.find_all('a')
        for i, pokemon in enumerate(ps):
            print(f'-> {region} [{i + 1}/{len(ps)}]')
            download_pokemon_picture(head + pokemon['href'], path)
    except:
        print(f'===> Error with {url}')


def download_by_region():
    soup = get_soup_with_random_session('https://bulbapedia.bulbagarden.net/wiki/Category:Pok%C3%A9mon_by_region')
    rs = soup.find('div', attrs={'class': 'mw-category'}).find_all('a')
    print(rs)
    head = 'https://bulbapedia.bulbagarden.net'
    for i, r in enumerate(rs):
        print(f'==> Region [{i + 1}/{len(rs)}]')
        print(r['href'])
        download_region(head + r['href'])


if __name__ == '__main__':
    download_by_region()

from downloader import get_soup_with_random_session, download_file_inside_path

from pathlib import Path


def download_all_episodes(link, anime_name='', path=Path.home()):
    try:
        soup = get_soup_with_random_session(link)
        ul = soup.find('ul', attrs={'class': 'episodes range active'})
        li_s = ul.find_all('li', attrs={'class': 'episode'})
        n_episodes = len(li_s)
        for k, li in enumerate(li_s):
            try:
                print(f'-> Downloading episode [{k + 1}/{n_episodes}]')
                ep_link = 'https://www.animeworld.tv' + li.a['href']
                download_episode(ep_link, anime_name=anime_name)
                print('Done!')
            except:
                print(f'  ===> Error with episode {k + 1} -> {ep_link}')
    except Exception as e:
        print(f'===> {e}')


def download_episode(ep_link, anime_name='', episode_number=0, path=Path.home()):
    # soup = get_soup_with_random_session(ep_link)
    # ep_video_link = soup.find('div', attrs={'id': 'player'}).video.source['src']
    # print(ep_video_link)
    download_file_inside_path(ep_link, f'{str.lower(anime_name)}_{episode_number}.mp4', path=path)


def main():
    if Path.home() / 'Anime' not in Path.home().iterdir():
        Path.mkdir(Path.home() / 'Anime')
    anime_name = input('Insert the name of the anime you want to download:\n-> ')
    anime_link = input('Insert its first episode\'s link in Animeworld.tv:\n-> ')
    if Path.home() / 'Anime' / anime_name not in Path(Path.home() / 'Anime').iterdir():
        Path.mkdir(Path.home() / 'Anime' / anime_name)
    path = Path.home() / 'Anime' / anime_name
    download_all_episodes(anime_link, anime_name=anime_name, path=path)


def recovery_downloading():
    for k in range(45):
        k = k+1
        if k < 10:
            link = f'http://www.drstone.cloud/DDL/ANIME/Georgie/Georgie_Ep_0{k}_ITA.mp4'
        else:
            link = f'http://www.drstone.cloud/DDL/ANIME/Georgie/Georgie_Ep_{k}_ITA.mp4'
        try:
            print(f'Downloading [{k}/{45}]')
            download_episode(ep_link=link, anime_name='Georgie', episode_number=k, path=Path(Path.home()/'Anime'/'Georgie'))
            print('Done!')
        except:
            print(f'Error: {link}')


if __name__ == '__main__':
    # main()
    recovery_downloading()



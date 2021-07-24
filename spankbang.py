from downloader import (get_soup_with_random_session,
                        download_file, insert_list_items,
                        hash)


def download_single_clip(url):
    try:
        soup = get_soup_with_random_session(url)
        video_link = soup.find('video').source['src']
        raw_title = soup.find('title').text
        title = hash(url + raw_title)[:8]
        print(title)
        download_file(video_link, title)
    except:
        print('Error')


def download_list_clips(list_urls):
    for i, url in enumerate(list_urls):
        print(f'[{i+1}/{len(list_urls)}] -> {url}')
        download_single_clip(url)
        print('Ok!')


if __name__ == '__main__':
    print('Welcome in SpankBang  ;)')
    items = insert_list_items()
    print(items)
    download_list_clips(items)

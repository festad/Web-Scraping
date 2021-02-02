from downloader import get_soup, download_list_files, get_chrome_driver
from pathlib import Path
import os
import sys
import re
from hashlib import sha256
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


p = re.compile(r'folder/[0-9]+')
pname = re.compile(r'([0-9a-zA-Z]+)')

driver = get_chrome_driver(headless=True)


def path_check():
	os.chdir(Path.home())
	if 'Cda' not in os.listdir():
		os.makedirs('Cda')
	os.chdir('Cda')


def download_list_folders(list_folders, list_names):
	for k in range(len(list_folders)):
		print(f'handling folder -> {list_folders[k]}')
		download_folder(list_folders[k], list_names[k])
		

def download_folder(folder, name):
	# folder_code = sha256(folder.encode('utf-8')).hexdigest()
	if name not in os.listdir():
		os.makedirs(name)
	os.chdir(name)
	k = 1
	videos_urls = []
	videos_names = []
	while True:
		soup = get_soup(f'{folder}/{k}')
		video_tags = soup.find_all('span',\
			attrs={'class':'wrapper-thumb-link mini-space-bottom hidden-viewList'})
		if len(video_tags) == 0:
			break
		for v in video_tags:
			video_url = 'https://www.cda.pl' + v.a['href']
			url_and_name = retrieve_video(video_url)
			videos_urls.append(url_and_name[0])
			videos_names.append(url_and_name[1])
		k += 1
	download_list_files(videos_urls, videos_names)
	os.chdir('..')
	
	
def retrieve_video(url):
	driver.get(url)
	vid_tag = WebDriverWait(driver, 40).until( \
		EC.presence_of_element_located((By.CLASS_NAME, 'pb-video-player')))
	video_src = vid_tag.get_attribute('src')
	soup = get_soup(url)
	raw_video_name = soup.find(attrs={'property': 'og:title'})['content']
	video_name = '-'.join(chunk for chunk in pname.findall(raw_video_name)) + f".{video_src.split('.')[-1]}"
	print(f'{video_name}')
	return (video_src, video_name)
	

def strip_code_from_url(folder):
	return p.match(folder).group(0)[7:]
	
	
if __name__ == '__main__':
	path_check()
	if len(sys.argv) < 2:
		print('Insert cda folder link as an argument')
		sys.exit()
	download_list_folders(sys.argv[1::2], sys.argv[2::2])

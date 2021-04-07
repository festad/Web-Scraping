import argparse
from downloader import get_soup, download_list_files, get_firefox_driver
from hashlib import sha256
import os
from pathlib import Path
import re
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from time import sleep


#parser = argparse.ArgumentParser()
#parser.add_argument('link', nargs='+', help='link to the folder on www.cda.pl')
#args = parser.parse_args()


p = re.compile(r'folder/[0-9]+')
pname = re.compile(r'([0-9a-zA-Z]+)')

#driver = get_firefox_driver(headless=False)

#counter_age_format_already_done = False


def path_check():
	os.chdir(Path.home())
	if 'Cda' not in os.listdir():
		os.makedirs('Cda')
	os.chdir('Cda')


def download_list_folders(list_folders):
	for k in range(len(list_folders)):
		print(f'handling folder -> {list_folders[k]}')
		download_folder(list_folders[k])
		

def download_folder(folder):
	folder_code = sha256(folder.encode('utf-8')).hexdigest()
	name = folder_code
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
			# videos_urls.append(url_and_name[0])
			# videos_names.append(url_and_name[1])
			download_file(url_and_name[0], url_and_name[1])
		k += 1
	# download_list_files(videos_urls, videos_names)
	os.chdir('..')
	
	
def download_page(page_link):
	# print(page_link)
	# return
	soup = get_soup(page_link)
	video_tags = soup.find_all('a', attrs='link-title-visit')
	for v in video_tags:
		print(v['href'])
		video_url = 'https://www.cda.pl' + v['href']
		print(video_url)
		url_and_name = retrieve_video(video_url)
		download_file(url_and_name[0], url_and_name[1])
	
	
def retrieve_video(url):
	driver = get_firefox_driver(headless=False)
	driver.get(url)
	
	compile_form_for_age(driver)
	
	vid_tag = WebDriverWait(driver, 40).until( \
		EC.presence_of_element_located((By.CLASS_NAME, 'pb-video-player')))
	video_src = vid_tag.get_attribute('src')
	soup = get_soup(url)
	raw_video_name = soup.find(attrs={'property': 'og:title'})['content']
	video_name = '-'.join(chunk for chunk in pname.findall(raw_video_name)) \
		+ f".{video_src.split('.')[-1]}"
	print(f'{video_name}')
	driver.quit()
	return (video_src, video_name)
	

def strip_code_from_url(folder):
	return p.match(folder).group(0)[7:]


def download_file(url, name):
	r = requests.get(url, stream=True)
	with open(name, 'wb') as f:
		for byte_chunk in r.iter_content(chunk_size=4096):
			f.write(byte_chunk)
			
			
def compile_form_for_age(driver):
	#global counter_age_format_already_done
	
	#if counter_age_format_already_done:
	#	return

	driver.implicitly_wait(20)
	try:
		dzien = driver.find_element_by_xpath("//select[@id='dzien']/option[@value='1']")
		print("You need to have a certain age!!")
		dzien.click()
		#sleep(3)
		driver.find_element_by_xpath("//select[@id='miesiac']/option[@value='1']").click()
		#sleep(3)
		driver.find_element_by_xpath("//select[@id='rok']/option[@value='1998']").click()
		#sleep(3)
		driver.find_element_by_xpath("//form/p/input").click()
		driver.find_element_by_xpath("//form/p/button").click()
		#counter_age_format_already_done = True
	except:
		print("No minimum age needed...")


if __name__ == '__main__':
	path_check()
	print(args.link)
	download_page(args.link)
	# download_list_folders(args.link)

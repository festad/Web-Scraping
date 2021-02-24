import argparse
from downloader import get_soup, download_list_files, get_chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


driver = get_chrome_driver(headless=True)


def main():
	news = get_news()
	print(news[1])
	
	
def get_news():
	url = 'https://wyborcza.pl/0,173236.html'
	driver.get(url)
	driver.implicitly_wait(10)
	news = []
	news_tags = driver.find_elements_by_xpath("//div[@class='body']/ul/li")
	for nt in news_tags:
		author = nt.find_element_by_class_name('author').find_element_by_tag_name('a').text
		title  = nt.find_element_by_tag_name('h3').find_element_by_tag_name('a').text
		lead   = nt.find_element_by_tag_name('p').text
		date   = nt.find_element_by_class_name('when').text
		link   = nt.find_element_by_tag_name('h3').find_element_by_tag_name('a').get_attribute('href')
		news.append((author,title,lead,date,link))
	news_str = ''
	k = 1
	tot = len(news)
	for n in news:
		news_str += f"{n[0]}\n\n{n[1]}\n\n{n[2]}\n\n{n[3]}\n\nlink -->{n[4]}\n\n[{k}/{tot}]\n{'='*20}\n\n"
		k += 1
	return (news, news_str)
	
	
def handle_article(url):
	driver.get(url)
	driver.implicitly_wait(10)
	author = driver.find_element_by_xpath("//span[@class='art-author']").text
	title  = driver.find_element_by_xpath("//*[@class='art-title']").text
	time   = driver.find_element_by_xpath("//*[@class='art-datetime']").text
	lead   = driver.find_element_by_xpath("//*[@class='article-lead']").text
	body   = ''
	for par in driver.find_elements_by_xpath("//*[@class='art_paragraph']"):
		body += f'{par.text}\n\n'
	art = (author,title,time,lead,body)
	art_str = f"{'='*30}\n{author}\n{title}\n{time}\n{'='*30}\n\n{lead}\n\n{body}{'~'*20}"
	return (art,art_str)
	
	
def news_to_article(news):
	return handle_article(news[4])


if __name__ == '__main__':
	main()

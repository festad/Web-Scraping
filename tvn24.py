import argparse
from bs4 import BeautifulSoup
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QApplication, 
	QMainWindow, 
	QVBoxLayout, 
	QWidget, 
	QPushButton, 
	QTextBrowser, 
	QScrollArea)
import requests
import requests_random_user_agent
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--selenium', action='store_true', help='use selenium')
parser.add_argument('-n', '--number-of-pages', type=int)
args = parser.parse_args()

if args.selenium:
	from downloader import get_chrome_driver, get_firefox_driver
	driver = get_firefox_driver(headless=True)


link = 'https://tvn24.pl/polska/'


class TopNews():
	def __init__(self, npages=1):
		if npages is None:
			npages = 2
		#self.outer_dates_tags  = []
		
		#self.outer_titles_links_tags = []
		
		self.pre_articles = generate_pre_articles_bs4(npages)
		
		#self.outer_links_tags  = []
		#for p in range(npages):
		#	print(f'\n\nhandling -> {link}{p+1}')
		#	driver.get(f'{link}{p+1}')
			
			#titles_links_tags = driver.find_elements_by_xpath(\
			#	"//div[@class='teaser-wrapper']/" + \
			#	"article/div[@class='link']/" + \
			#	"div[@class='link__content']/a")
			
			#titles_links_tags = find_titles_links_bs4(f'{link}{p+1}')
			
			#for i in range(len(titles_links_tags)):
			#	print( \
			#		f"{titles_links_tags[i].get_attribute('title')[11:]}\n"
			#	)
			#		#f"{titles_links_tags[i].get_attribute('href')}\n\n"
					
				#self.outer_titles_links_tags.append(titles_links_tags[i])
				
			#	self.pre_articles.append(PreArticle( \
			#		titles_links_tags[i]['title'][11:], \
			#		titles_links_tags[i]['href']
			#		)
			#	)
					
# TODO:
#	class PreArticle -> title, link -> ...

def generate_pre_articles_bs4(npages):
	pre_articles = []
	for n in range(npages):
		link = f'https://tvn24.pl/polska/{n+1}'
		session = requests.Session()
		soup = BeautifulSoup(session.get(link).text, 'lxml')
		tags = soup.find_all('div',  attrs={'class':'teaser-wrapper'})
		titles_links_tags = []
		k = 1
		for tag in tags:
			try:
				titles_links_tags.append(tag.findChild('article') \
					.findChild('div', attrs={'class':'link'}) \
					.findChild('div', attrs={'class':'link__content'}) \
					.findChild('a'))
			except:
				print(f'Article {k} of page {n+1} gave problems')
			finally:
				k += 1
			
		for i in range(len(titles_links_tags)):
			pre_articles.append(PreArticle( \
				titles_links_tags[i]['title'][11:], \
				titles_links_tags[i]['href']
				)
			)
	return pre_articles
	




class ArticleScraper():
	def __init__(self, link):
		session = requests.Session()
		soup = BeautifulSoup(session.get(link).text, 'lxml')
		#driver.get(link)
		
		self.title = soup.find('div', attrs={'class':'article-story-header'}) \
			.find('div') \
			.find('h1').text.upper()
			
		print(f"Truth about attrs: {soup.find('div', attrs={'class':'article-story-header'}).attrs}")
			
		#self.title = driver.find_element_by_xpath( \
		#	"//div[@class='article-story-header']/" + \
		#	"div/h1").text
		
		self.date_tag = soup.find('time', \
			attrs={'class':'article-top-bar__date'})
		
		#self.date_tag = driver.find_element_by_xpath(\
		#	"//time[@class='article-top-bar__date']"
		#)
		
		self.header = soup.find('div', \
			attrs={'class':'article-story-content__elements'}) \
			.find('div') \
			.find('p', attrs={'class':'lead-text'})
			
		#self.header = driver.find_element_by_xpath(\
		#	"//div[@class='article-story-content__elements']/" + \
		#	"div/p[@class='lead-text']"
		#)
		
		candidate_paragraphs = soup.find('div', \
			attrs={'class':'article-story-content__elements'}) \
			.find_all('div')
		print(f'candidate paragraphs: #{len(candidate_paragraphs)}')
		self.paragraphs = []
		for cp in candidate_paragraphs:
			if 'class' in cp.attrs:
				print(cp.attrs['class'])
				if 'article-element--paragraph' in \
					cp.attrs['class'] \
				or 'article-element--subhead' in \
					cp.attrs['class']:			
					self.paragraphs.append(cp)
				
		#self.paragraphs = driver.find_elements_by_xpath( \
		#	"//div[@class='article-story-content__elements']/" + \
		#	"div[@class='article-element article-element--paragraph' " + \
		#	"or @class='article-element article-element--subhead']"
		#)
		#for p in self.paragraphs:
		#	print(f'{p.text}')
		
		body_str = ''
		for p in self.paragraphs:
			if 'article-element--paragraph' \
				in p['class']:
				
				body_str += p.text + '\n\n'
			else:
				body_str += p.text.upper() + '\n\n'
		self.body = self.header.text + "\n\n" + body_str
	
	
	def generate_article(self):
		return Article(self.title, self.date_tag.text, self.body)

			
class PreArticle():
	def __init__(self, title, link):
		self.title = title
		self.link  = link


class Article():
	def __init__(self, title, date, body):
		self.title  = title
		self.date   = date
		self.body   = body



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("TVN24 - Polska")
		self.setGeometry(100, 100, 800, 600)
		
		self.scroll = QScrollArea()
		self.layout = QVBoxLayout()
		
		widget = QWidget()
		widget.setLayout(self.layout)
		
		self.scroll.setWidgetResizable(True)
		self.scroll.setWidget(widget)
		self.setCentralWidget(self.scroll)
		
		self.current_article_window = None
		
		
	def add_button_with_text(self, pre_article):
		#print(pre_article.link)
		button_title = f'{pre_article.title}'
		button = QPushButton(button_title)
		button.clicked.connect(lambda: self.button_action(pre_article))
		self.layout.addWidget(button)
		
		
	def update_window(self, list_pre_articles):
		self.layout = QVBoxLayout()
		for pa in list_pre_articles:
			self.add_button_with_text(pa)

		
	def button_action(self, pre_article):
		article = ArticleScraper(pre_article.link).generate_article()
		print('\n\n' + article.body)
		self.current_article_window = ArticleWindow(article)
		self.current_article_window.show()
		
		
class ArticleWindow(QWidget):
	def __init__(self, article):
		super().__init__()
		layout = QVBoxLayout()
		textbrowser = QTextBrowser()
		article_text = f"{article.title}\n\n{article.date}\n\n{'='*50}\n\n{article.body}"
		textbrowser.setPlainText(article_text)
		layout.addWidget(textbrowser)
		self.setWindowTitle(article.title)
		self.setLayout(layout)
		self.setGeometry(150, 150, 600, 600)
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()

	top_news = TopNews(npages=args.number_of_pages)
	for pa in top_news.pre_articles:
		window.add_button_with_text(pa)

	window.show()

#while True:
#	top_news = TopNews(npages=1)
#	window.update_window(top_news.pre_articles)
#	time.sleep(20)

	app.exec_()

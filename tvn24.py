from downloader import get_chrome_driver, get_firefox_driver, get_soup
from bs4 import BeautifulSoup


driver = get_firefox_driver(headless=True)


link = 'https://tvn24.pl/polska/'


class TopNews():
	def __init__(self, npages=2):
		#self.outer_dates_tags  = []
		
		self.outer_titles_links_tags = []
		self.pre_articles = []
		
		#self.outer_links_tags  = []
		for p in range(npages):
			driver.get(f'{link}{p+1}')
			
			titles_links_tags = driver.find_elements_by_xpath(\
				"//div[@class='teaser-wrapper']/" + \
				"article/div[@class='link']/" + \
				"div[@class='link__content']/a")
			
			for i in range(len(titles_links_tags)):
				print( \
					f"{titles_links_tags[i].get_attribute('title')[11:]}\n" + \
					#f"{titles_links_tags[i].get_attribute('href')}\n\n"
				)
				self.outer_titles_links_tags.append(titles_links_tags[i])
				
				self.pre_articles.append(PreArticle( \
					titles_links_tags[i].get_attribute('title')[11:], \
					titles_links_tags[i].get_attribute('href')
					)
				)
					
# TODO:
#	class PreArticle -> title, link -> ...

class ArticleScraper():
	def __init__(self, link):
		driver.get(link)
		self.title = driver.find_element_by_xpath( \
			"//div[@class='article-story-header']/" + \
			"div/h1").text
		self.date_tag = driver.find_element_by_xpath(\
			"//time[@class='article-top-bar__date']"
		)
		self.header = driver.find_element_by_xpath(\
			"//div[@class='article-story-content__elements']/" + \
			"div/p[@class='lead-text']"
		)
		self.paragraphs = driver.find_elements_by_xpath( \
			"//div[@class='article-story-content__elements']/" + \
			"div[@class='article-element article-element--paragraph' " + \
			"or @class='article-element article-element--subhead']"
		)
		#for p in self.paragraphs:
		#	print(f'{p.text}')
		body_str = ''
		for p in self.paragraphs:
			if p.get_attribute('class') == \
				'article-element article-element--paragraph':
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




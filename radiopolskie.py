from downloader import get_chrome_driver


driver = get_chrome_driver(headless=True)


# https://www.polskieradio.pl/395/7989/Artykul/2684663,Nearly-276-million-COVID19-shots-administered-in-Poland-govt-data


class Article():
	def __init__(self, link):
		driver.get(link)
		self.title = driver.find_element_by_xpath("//*[@class='no-border']/*[@class='title']").text
		self.datetime = driver.find_element_by_xpath("//*[@class='time'][@id='datetime2']").text
		body_list = [body_tag.text for body_tag in \
			driver.find_elements_by_xpath( \
			"//div[@class='content']/span/p")]
		self.body = '\n\n'.join(body_list)


class TopNews():
	def __init__(self, link):
		driver.get(link)
		articles_tags = driver.find_elements_by_xpath("//div[@class='all-articles']/*[@class='article']")
		self.pre_articles = [PreArticle(a_t) for a_t in articles_tags]
		
		
class PreArticle():
	def __init__(self, article_tag):
		a_tag = article_tag.find_element_by_tag_name('a')
		self.link = a_tag.get_attribute('href')
		self.title = a_tag.get_attribute('title')
		self.datetime = a_tag.find_element_by_class_name('date').text
		
	
	def get_full_article(self):
		return Article(self.link)

from bs4 import BeautifulSoup

import requests
import requests_random_user_agent


def _get_soup_with_random_session(url):
	session = requests.Session()
	return BeautifulSoup(session.get(url).text, 'lxml')
	

class Hentai():
	def __init__(self, hentai_code):
		self.hentai_code = hentai_code
		self.url = f'https://nhentai.net/g/{hentai_code}'
		self.npages = self._retrieve_number_of_pages()
		
		
	def _retrieve_number_of_pages(self):
		soup = _get_soup_with_random_session(self.url)
		tags_field = soup.find_all('div', attrs={'class':'tag-container field-name'})
		for t in tags_field:
			if 'Pages' in t.text:
				tag = t
		npages = tag.findChild('span').findChild('a').findChild('span').text
		return int(npages)
		
		
	def _retrieve_page_number_(self, n):
		soup = _get_soup_with_random_session(f'{self.url}/{n}')
		img_source = soup.find('section', attrs={'id':'image-container'}) \
			.findChild('a').findChild('img')['src']
		return img_source
		
		
	def _download_page(self, n):
		r = requests.Session().get(self._retrieve_page_number_(n))
		with open(f'{self.hentai_code}-{n}.jpg', 'wb') as f:
			for byte_chunk in r.iter_content(chunk_size=4096):
				f.write(byte_chunk)
				
				
	def download_hentai(self):
		for k in range(self.npages):
			self._download_page(k+1)

import requests
from bs4 import BeautifulSoup


def get_soup_from_dictionary(query):
    url = f'https://sjp.pwn.pl/szukaj/{query}.html'
    return BeautifulSoup(requests.get(url).text, features='lxml')


def prettify_soup(soup, query):
    answer = ''
    if soup.find(attrs={'class': 'sugestie'}):
        answer += f'Nie znaleziono żadnych wyników wyszukiwania dla: {query}\n'
        answer += 'Czy chodziło Ci o:\n'
        for sugestie in soup.find(attrs={'class': 'sugestie'}).findChildren('a'):
            answer += (sugestie.text + '\n')
        return answer
    answer += '-----------------------'
    answer += '\nOgólne informacje'
    answer += '\n---------------------\n'
    for entry in soup.find_all(attrs={'class': 'entry'}):
        if 'Słowniki PWN - zobacz ofertę' in entry.text:
            break
        answer += (entry.text.strip() + '\n')
    if soup.find(attrs={'class': 'entry'}):
        if soup.find(attrs={'class': 'entry'}).findChild('a'):
            answer += '\n---------------------'
            answer += '\nPodobne wyszukiwania'
            answer += '\n---------------------\n'
            for podobne in soup.find(attrs={'class': 'entry'}).findChildren('a'):
                answer += (podobne.text + '\n')
    if soup.find('article'):
        if soup.find('article').findChild(attrs={'class': 'tytul'}):
            answer += '\n---------------------'
            answer += '\nSynonimy'
            answer += '\n---------------------\n'
            for synonim in soup.find('article').findChildren(attrs={'class': 'tytul'}):
                answer += (synonim.a['pwn-search'])
                if synonim.parent.findChild(attrs={'class': 'glosa'}):
                    answer += synonim.parent.findChild(attrs={'class': 'glosa'}).text
                for li in synonim.parent.ul.findChildren('li'):
                    answer += ('\n -> ' + li.a.text)
                answer += '\n'
    return answer + '\n'


if __name__ == '__main__':
    while True:
        query = input("What word are you interested in?\n-> ")
        print(prettify_soup(get_soup_from_dictionary(query), query))

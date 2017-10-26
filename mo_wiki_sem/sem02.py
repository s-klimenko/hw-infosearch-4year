import re
import requests
from bs4 import BeautifulSoup


def ro_wiki(query, done, todo):
    """
    Scrapes links to wiki pages
    :param query: link to article
    :param done: already visited articles
    :param todo: links from this page
    :return: -
    """
    print(len(done), query)
    url = 'https://mo.wikipedia.org{}'.format(query)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    todo = set([a['href'] for a in soup.findAll('a', attrs={'href': re.compile('^/wiki/')})])
    todo = [link for link in todo if re.search('[:.]', link) is None]
    done.append(query)
    for link in todo:
        if link not in done:
            todo.pop(0)
            ro_wiki(link, done, todo)


def get_links():
    """
    Creates empty lists for initial run of ro_wiki.py
    :return: list with all the articles
    """
    done = []
    todo = []
    ro_wiki('', done, todo)
    return done


def links_to_txt():
    """
    Writes links in the .txt file
    :return: -
    """
    all_links = get_links()
    with open('mo_wiki.txt', 'w', encoding='utf-8') as f:
        result = ['{}. {}'.format(inx, link) for inx, link in enumerate(all_links, start=1)]
        text = '\n'.join(result)
        f.write(text)


links_to_txt()

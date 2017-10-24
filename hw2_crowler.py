import requests
from bs4 import BeautifulSoup
import os
import re


def get_article(link):
    """
    Scrapes articles and meta-info and writes them into txt files
    :param link: link to the article
    :return: True if success, else - False
    """
    try:
        url = 'http://ngisnrj.ru{}'.format(link)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        try:
            for br in soup.find_all("br"):
                br.replace_with("\n")
            soup = soup.find('div', {'class': 'b-object__detail'})
            pre_text = soup.find('div', {'class': 'b-object__detail__annotation'}).get_text().strip('\r\n').strip('\t')
            text = soup.find('div', {'class': 'b-block-text__text'}).get_text().strip('\r\n').strip('\t')
            all_text = pre_text + '\r' + text
            try:
                author = soup.find('span', {'class': 'b-object__detail__author__name'}).get_text().strip('\r\n')\
                    .strip('\t')
            except TypeError:
                author = 'Noname'
            title = soup.find('h1').get_text().strip('\r\n')
            info = soup.find('div', {'class': 'b-basic-info__content'})
            date = info.find('span', {'class': 'date'}).get_text().strip('\r\n')
            tags = info.find('div', {'class': 'b-category-list-inline-2'})
            all_tags = tags.find_all('a')
            tags = ', '.join(map(lambda x: x.get_text(), all_tags))
            global numb
            numb += 1
            with open('./corpora/ngisnrj{}.txt'.format(str(numb)), 'w', encoding='utf-8') as f:
                f.write('@au ' + author + '\r@ti ' + title + '\r@da ' +
                        date + '\r@topic ' + tags + '\r@url ' + url + '\r' + all_text)
            return True
        except AttributeError:
            return False
    except requests.exceptions.ConnectionError:
        return False


def get_links(page, links_set):
    """
    Crawls through pages, scrapes links to the articles, passes them to get_article func and writes in links_set
    :param page: link to web-page with articles
    :param links_set: set with already scraped links
    :return: -
    """
    global numb
    if numb < 1000:
        url = 'http://ngisnrj.ru{}'.format(page)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        soup = soup.find('div', {'class': 'b-layout01__col2'})
        next_page = soup.find('a', {'class': 'b-paginator__next'})
        articles = soup.find_all('h2', {'class': 'b-object__list__item__title'})
        for i in articles:
            i = i.find('a')
            if i['href'] not in links_set:
                is_true = get_article(link=i['href'])
                if is_true:
                    links_set.add(i['href'])
        if next_page:
            get_links(next_page['href'], links_set)
    else:
        quit()


def get_categories(corpus):
    """
    Scrapes categories links and crawls trough them
    :param corpus: empty list or, if restarted, list with scraped articles
    :return: -
    """
    links_set = set(corpus)
    categories = ["/news/?category=obschestvo", "/news/?category=obrazovanie", "/news/?category=kultura",
                  "/news/?category=sport", "/news/?category=pravo-i-zakon", "/news/?category=selskoe-hozyajstvo",
                  "/news/?category=sotsialnoe-partnerstvo", "/news/?category=trud-i-zanyatost",
                  "/news/?category=ekologiya", "/news/?category=politika", "/news/?category=meditsina",
                  "/news/?category=stroitelstvo", "/news/?category=transport", "/news/?category=ekonomika",
                  "/news/?category=promyishlennost", "/news/?category=energetika", "/news/?category=turizm",
                  "/news/?category=zhkh", "/news/?category=malyij-i-srednij-biznes", "/news/?category=proisshestviya",
                  "/news/?category=smi", "/news/?category=informatsionnyie-tehnologii", "/news/?category=nauka"]
    for link in reversed(categories):
        print('скачиваю статьи из {}'.format(link))
        get_links(page=link, links_set=links_set)


def get_downloaded_links(filename):
    """
    Returns empty string if corpus is empty or url of downloaded article
    :param filename: name of file with article or empty string
    :return: url or empty string
    """
    with open('./corpus/'+filename, 'r', encoding='utf-8') as f:
        f = f.read()
        res = re.search('@url (.*?)\n', f)
        return res.group(1)


my_corpus = [get_downloaded_links(filename) for filename in os.listdir('.\corpus')]
numb = len(my_corpus)
get_categories(corpus=my_corpus)

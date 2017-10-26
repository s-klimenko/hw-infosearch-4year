from collections import defaultdict
from pymystem3 import Mystem  # импортируем майстем
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import time
from collections import Counter
import json
import os


def text_to_list(text, m):
    """
    Превращает текст в список лемм
    :param text: текст
    :type text: str
    :param m: экземпляр класса-анализатора MyStem
    :return: список лемм
    :rtype: list
    """
    punct = punctuation
    punct += "0123456789–—«»`'"
    stop_words = stopwords.words('russian')
    lemmas = m.lemmatize(text)
    text = ''.join(map(lambda lemma: lemma.strip('«»'), lemmas))
    tokens_with_punct = word_tokenize(text)
    tokens = [token for token in tokens_with_punct if token not in punct]  # удаляем пунктуацию
    tokens = [token for token in tokens if token not in stop_words]  # удаляем стоп-слова
    return tokens


def texts_to_index(docs_as_lists):
    """
    Превращает список списков лемм в обратный индекс
    :param docs_as_lists: массив массивов с леммами
    :type docs_as_lists: list
    :return: index - словарь формата {лемма : список словарей {doc_name - документ, freq - частота леммы в документе}}
    doc_len - словарь формата {документ : длина}
    :rtype: dict
    """
    index = defaultdict(list)
    doc_info = {}
    for doc in docs_as_lists:
        doc_lems = doc[0]
        doc_name = doc[1]
        c = Counter(doc_lems)
        dl = sum(c.values())
        doc_info[doc_name] = dl
        for word in set(doc_lems):
            freq = c[word]/dl
            index[word].append({'doc_name': doc_name, 'freq': freq})
    return index, doc_info


def inverted_id(corpora):
    """
    Создает обратный индекс термов по корпусу
    :param corpora: список путей к текстовым документам
    :type corpora: list
    :return: текстовый файл с обратным индексом
    """
    global time0
    print('Начинаю обработку...')
    print(time.time() - time0)
    m = Mystem()  # создаем экземпляр класса-анализатора
    lemma_corpora = []
    doc_info_links = {}
    n = 0
    for doc in corpora:
        n += 1
        if n % 10 == 0:
            print('Обрабатываю {}...'.format(doc))
            print(time.time()-time0)
        f = open(doc, 'r', encoding='utf-8')
        big_text = f.readlines()
        text = ''.join(big_text[5:])
        doc_name = big_text[1].strip('@ti ').strip('\n')
        link = big_text[4].strip('@url ').strip('\n')
        doc_info_links[doc_name] = link
        lemma_corpora.append([text_to_list(text, m), doc_name])
    print('Преобразовываю в индекс...')
    print(time.time() - time0)
    index, doc_info_length = texts_to_index(lemma_corpora)
    doc_info = {k: {'link': doc_info_links[k], 'len': doc_info_length[k]} for k in doc_info_links}
    print('Записываю файлы...')
    print(time.time() - time0)
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(index, ensure_ascii=False))
    with open('doc_info.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(doc_info, ensure_ascii=False))


def get_inverted_index():
    """
    Gets corpus for inverted index
    :return: -
    """
    print('Собираю корпус...\r')
    for d, dirs, files in os.walk('./corpus'):
        corpus = ['./corpus/{}'.format(f) for f in files]
    inverted_id(corpus)

if __name__ == '__main__':
    time0 = time.time()
    get_inverted_index()
    print('Индекс готов!')
    print('---{}---'.format(time.time() - time0))

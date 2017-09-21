from collections import defaultdict
from pymystem3 import Mystem  # импортируем майстем
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def text_to_list(text, m):
    '''
    Превращает текст в список лемм без повторения
    :param text: текст
    :type text: str
    :param m: экземпляр класса-анализатора MyStem
    :return: список лемм
    :rtype: list
    '''
    punct = punctuation
    punct += "0123456789–—«»`'"
    stop_words = stopwords.words('russian')
    lemmas = m.lemmatize(text)
    text = ''.join(lemmas)
    tokens_punct = set(word_tokenize(text))
    tokens = list(set(token for token in tokens_punct if token not in punct)) #удаляем пунктуацию
    tokens = list(set(token for token in tokens if token not in stop_words)) #удаляем стоп-слова
    return tokens

def texts_to_index(docs_as_lists):
    '''
    Превращает список списков лемм в обратный индекс
    :param docs_as_lists: массив массивов с леммами
    :type docs_as_lists: list
    :return: словарь формата {лемма : список номеров документов}
    :rtype: dict
    '''
    d = defaultdict(list)
    n = 0
    for doc in docs_as_lists:
        n += 1
        doc = set(doc)
        for word in doc:
            d[word] += [str(n)]
    return d

def inverted_id(corpora):
    '''
    Создает обратный индекс термов по корпусу
    :param corpora: список путей к текстовым документам
    :type corpora: list
    :return: текстовый файл с обратным индексом
    '''
    m = Mystem()  # создаем экземпляр класса-анализатора
    lemma_corpora = []
    for doc in corpora:
        f = open(doc, 'r', encoding='utf-8')
        text = f.read()
        lemma_corpora.append(text_to_list(text, m))
    index = texts_to_index(lemma_corpora)
    f = open('result.txt', 'w', encoding='utf-8')
    for id in index:
        print(id, index[id])
        string = (id + ' ' + str(index[id]) + '\n')
        f.write(string)
    f.close()

corpora = ['1.txt', '2.txt']
inverted_id(corpora)

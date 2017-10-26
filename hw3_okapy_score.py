from pymystem3 import Mystem
from math import log
import json
from hw3_index import text_to_list
from collections import defaultdict, Counter


def score_BM25(n, fq, dl, avdl=337.9792349726776, N=915):
    """
    Okapi BM25 score
    :param n: quantity of documents with word q
    :param fq: frequency of word q in document D
    :param N: size of corpus in documents
    :param dl: length of document D
    :param avdl: average length of document in corpus
    :return: relevancy score
    """
    k1 = 2.0
    b = 0.75
    K = compute_K(dl, avdl, k1, b)
    IDF = log((N - n + 0.5) / (n + 0.5))
    frac = ((k1 + 1) * fq) / (K + fq)
    return IDF * frac


def compute_K(dl, avdl, k1, b):
    return k1 * ((1 - b) + b * (float(dl) / float(avdl)))


def get_avdl():
    """
    Returns average length of texts in corpus using pre-made document with info
    :return: average length of article
    """
    with open('doc_info.json', 'r', encoding='utf-8') as f:
        f = f.read()
        data = json.loads(f)
    x = [data[i]['len'] for i in data]
    return sum(x) / len(x)


def get_dl(doc):
    """
    Returns length of the article using pre-made document with info
    :param doc: title od the article in corpus
    :return: length of the article
    """
    with open('doc_info.json', 'r', encoding='utf-8') as f:
        f = f.read()
        data = json.loads(f)
    length = data[doc]['len']
    return length


def get_okapi(query):
    """
    Returns Okapi BM25 score for every document given word in corpus
    :param query:
    :return:
    """
    m = Mystem()
    query = text_to_list(query, m)  # list of lemmas
    with open('result_1.json', 'r', encoding='utf-8') as f:
        f = f.read()
        data = json.loads(f)
        total_score = defaultdict(int)
        for word in query:
            try:
                all_info = (data[word])
                n = (len(all_info))
                for article in all_info:
                    fq = article['freq']
                    dl = get_dl(article['doc_name'])
                    score = score_BM25(n=n, fq=fq, dl=dl)
                    total_score[article['doc_name']] += score
            except KeyError:
                pass
        result = sorted(total_score.items(), key=lambda x: x[1], reverse=True)[:10]
        return result


def get_link(title):
    """
    Returns link for title of article
    :param title: title of article
    :return: link
    """
    with open('doc_info.json', 'r', encoding='utf-8') as f:
        f = f.read()
        data = json.loads(f)
        link = data[title]['link']
        return link


def get_corpus_results(query):
    """
    Calculates Okapi for query and returns top-10 articles
    :param query: query
    :return: dict {html for link and title: score}
    """
    res = get_okapi(query)
    result = {}
    for idx, i in enumerate(res, start=1):
        a ='<a href="{}"><b>{}.</b> {}</a>'.format(get_link(i[0]), idx, i[0])
        score = i[1]
        result[a] = score
    return result


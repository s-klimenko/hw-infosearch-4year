import collections
import os
import re


def get_dubs():
    for d, dirs, files in os.walk('./corpus'):
        corpora = ['./corpus/{}'.format(f) for f in files]
        doc_names = []
        for doc in corpora:
            f = open(doc, 'r', encoding='utf-8')
            big_text = f.readlines()
            doc_name = big_text[1].strip('@ti ').strip('\n')
            doc_names.append(doc_name)
    c = collections.Counter(doc_names)
    x = [i for i in c if c[i] == 2]
    dict = {}
    for d, dirs, files in os.walk('./corpus'):
        corpora = ['./corpus/{}'.format(f) for f in files]
        doc_names = []
        for doc in corpora:
            f = open(doc, 'r', encoding='utf-8')
            big_text = f.readlines()
            doc_name = big_text[1].strip('@ti ').strip('\n')
            if doc_name in x:
                dict[doc] = doc_name
    for i in x:
        print(i)
        for j in dict:
            if dict[j] == i:
                print(j)


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


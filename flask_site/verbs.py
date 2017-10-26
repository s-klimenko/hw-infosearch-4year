from pymystem3 import Mystem  # импортируем майстем
from collections import Counter


def verbs_statistics(text):
    '''
    Выделяет из текста данные о частотности глаголов, их лемм, вида и совершенности
    :param text: текст
    :return: словари с частотностью
    '''
    m = Mystem()  # создаем экземпляр класса-анализатора
    ana = m.analyze(text)
    print(ana)
    print(len(ana))
    for i in ana:
        try:
            i['analysis']
            print(i)
        except KeyError: print(int())
    pos = [i['analysis'][0]['gr'].split('=')[0].split(',')[0] for i in ana if
           i['text'].strip() and 'analysis' in i and i['analysis']]
    verbs = [i['analysis'][0] for i in ana if i['text'].strip() and 'analysis' in i and i['analysis'] and
             i['analysis'][0]['gr'].split('=')[0].split(',')[0] == 'V']
    print(verbs)
    print(type(pos))
    all_pos, v, ratio = pos_counter(pos)
    lemms = lemma_counter(verbs)
    tr, intr = trans_couter(verbs)
    s, ns, amb = aspect_counter(verbs)
    return all_pos, v, ratio, lemms, tr, intr, s, ns, amb


def all_same(items):
    '''
        Проверяет все ли объекты в списке одинаковые
    :param items: список с объектами
    :type items: list
    :return: True - если все объекты одинаковые
    '''
    return all(x == items[0] for x in items)


def pos_counter(pos):
    '''
    Считает части речи, глаголы и долю глаголов в тексте.
    :param pos: список с частеречными тегами Mystem для всех слов в тексте
    :type pos: list
    :return: all_pos - количество всех частей речи (слов) в тексте
             v - количество глаголов в тексте
             ratio - доля глаголов в тексте
    '''
    c_pos = Counter(pos)
    all_pos = sum(c_pos.values())
    v = c_pos['V']
    if all_pos != 0:
        ratio = v / all_pos
    else: ratio = 0
    return all_pos, v, ratio


def lemma_counter(verbs):
    '''
    Считает количество лемм
    :param verbs:
    :type verbs: list
    :return: lemms - отсортированный по убыванию частотности словарь {лемма глагола : частотность в тексте}
    '''
    lemma = [i['lex'] for i in verbs]
    c_lem = Counter(lemma)
    lemms = {i[0]: str(i[1]) for i in c_lem.most_common()}
    return lemms


def trans_couter(verbs):
    '''
    Считает количество переходных и непереходных глаголов
    :param verbs:
    :type verbs: list
    :return: tr - количество переходных глаголов в тексте
             intr - количество непереходных глаголов в тексте
    '''
    trans = [j.split('=')[0] for i in verbs for j in i['gr'].split(',') if j.startswith('нп=') or j.startswith('пе=')]
    c_tr = Counter(trans)
    tr = c_tr['пе']
    intr = c_tr['нп']
    return tr, intr


def aspect_counter(verbs):
    '''
    Считает количество глаголов совершенного и несовершенного вида
    :param verbs:
    :return: s - количество глаголов совершенного вида в тексте
             ns- количество глаголов несовершенного вида в тексте
             amb- количество глаголов, вид которых не удалось определить однозначно
    '''
    aspect = []
    for i in verbs:
        aspect_small = [k for j in i['gr'].split('|') for k in j.split(',') if k == 'несов' or k == 'сов']
        if all_same(aspect_small) and aspect_small != []:
            print(aspect_small)
            aspect.append(aspect_small[0])
        elif not all_same(aspect_small) and aspect_small != []:
            aspect.append('amb')
    c_as = Counter(aspect)
    s = c_as['сов']
    ns = c_as['несов']
    amb = c_as['amb']
    return s, ns, amb

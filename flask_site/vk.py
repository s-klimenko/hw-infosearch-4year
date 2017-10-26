from pymystem3 import Mystem  # импортируем майстем
import requests
import json
import re
from verbs import lemma_counter


def check_error_vkAPI(response):
    '''
    Проверяет вернула ли VK API ошибку или нет
    :param response: ответ VK API
    :type response: json
    :return: текст ошибки, если она есть, False, если ее нет
    '''
    response = response.json()
    if 'error' in response.keys():
        if response['error']['error_code'] == 15:
            error = 'Отказано в доступе. Пожалуйста, введите ID или короткое имя открытого сообщества. :)'
        elif response['error']['error_code'] == 100:
            error = 'Ошибка в написании ID или короткого имени. Пожалуйста, попробуйте еще раз. :)'
        elif response['error']['error_code'] == 18:
            error = 'Группа удалена, забанена или еще не существует. Пожалуйста, введите ID или короткое имя другой группы. :)'
        else:
            error = 'Error message: %s. Error code: %s' % \
                    (response['error']['error_msg'], response['error']['error_code'])
    else:
        error = False
    return error


def clean_html(raw_html):
    '''
    Чистит html от тегов
    :param raw_html: html с тегами
    :type raw_html: str
    :return: чистый текст
    :rtype: str
    '''
    clean_r = re.compile('<.*?>')
    clean_text = re.sub(clean_r, '', raw_html)
    return clean_text


def count_words(posts, needed_pos=None):
    '''
    Считает леммы
    :param posts: текст
    :param needed_pos: части речи, леммы которых нужно посчитать
    :type posts: str
    :type needed_pos: list
    :return: отсортированный по убыванию частотности словарь {лемма глагола : частотность в тексте}
    :rtype: dict
    '''
    m = Mystem()  # создаем экземпляр класса-анализатора
    ana = m.analyze(posts)
    words = [i['analysis'][0] for i in ana if i['text'].strip() and 'analysis' in i and i['analysis']]
    if needed_pos is not None:
        words = [i for i in words if i['gr'].split('=')[0].split(',')[0] in needed_pos]
    return lemma_counter(words)

def get_vk_posts(id_or_name):
    '''
    Функция скачивает первые 1000 постов со стены группы (если постов меньше 1000, то скачивает все) и возвращает
    список частотных лемм. Если группа закрытая, возвращает текст ошибки.
    :param id_vk: ID группы или короткое имя
    :type id_vk: int or str
    :return: error_message - есть ли сообщение об ошибке, result - леммы или сообщение об ошибке
    :rtype: boolean, str
    '''
    all_posts = ''
    if type(id_or_name) == int:
        id_vk = id_or_name
    else:
        response = requests.get('https://api.vk.com/method/groups.getById?group_id={}'.format(str(id_or_name)))
        error_text = check_error_vkAPI(response)
        if not error_text:
            group_response = json.loads(response.text)
            id_vk = group_response['response'][0]['gid']
        else:
            print(response.json())
            error_message = True
            return error_message, error_text
    response = requests.get('https://api.vk.com/method/wall.get?owner_id=-{}&count=1'.format(str(id_vk)))
    error_text = check_error_vkAPI(response)
    if not error_text:
        for offset in range(0, 1001, 100):
            print(offset)
            response = requests.get('https://api.vk.com/method/wall.get?owner_id=-{}&count=10&offset={}'
                                    .format(id_vk, str(offset)))
            data = json.loads(response.text)
            for i in range(1, len(data['response'])):
                all_posts += clean_html(data["response"][i]["text"])
    else:
        error_message = True
        return error_message, error_text
    error_message = False
    result = count_words(all_posts, ['V', 'N', 'ADV', 'A'])
    return error_message, result

import requests
import time
import conf


def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    _url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/ocr'
    _maxNumRetries = 1

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)
        print(response.json())

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result


def get_text_from_image(url_image, is_handwriting):
    _key = conf.CVAPI_KEY_1

    # URL direction to image

    # Computer Vision parameters
    params = {'language': 'unk', 'detectOrientation': 'true', 'handwriting': is_handwriting}
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json'
    json = {'url': url_image}
    data = None

    result = processRequest(json, data, headers, params)

    if result is not None:
        all_lines = []
        lines = result['regions'][0]['lines']
        for i in range(len(lines)):
            words = lines[i]['words']
            text = (words[j]['text'] for j in range(len(words)))
            text_string = ' '.join(text) + '<br>'
            print(text_string)
            all_lines.append(text_string)
        return ''.join(all_lines)
    return 'Не удалось распознать текст :('

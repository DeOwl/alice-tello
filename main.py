
from flask import Flask, request
import logging


import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "РќРµ С…РѕС‡Сѓ.",
                "РќРµ Р±СѓРґСѓ.",
                "РћС‚СЃС‚Р°РЅСЊ!",
            ]
        }
        res['response']['text'] = 'РџСЂРёРІРµС‚! РљСѓРїРё СЃР»РѕРЅР°!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'Р»Р°РґРЅРѕ',
        'РєСѓРїР»СЋ',
        'РїРѕРєСѓРїР°СЋ',
        'С…РѕСЂРѕС€Рѕ'
    ]:
        res['response']['text'] = 'РЎР»РѕРЅР° РјРѕР¶РЅРѕ РЅР°Р№С‚Рё РЅР° РЇРЅРґРµРєСЃ.РњР°СЂРєРµС‚Рµ!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = 'Р’СЃРµ РіРѕРІРѕСЂСЏС‚ "%s", Р° С‚С‹ РєСѓРїРё СЃР»РѕРЅР°!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Р›Р°РґРЅРѕ",
            "url": "https://market.yandex.ru/search?text=СЃР»РѕРЅ",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
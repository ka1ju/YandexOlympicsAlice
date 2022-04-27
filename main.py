from flask import Flask, request
from oleg import *
from all_wallets import *
from create_delete_wallet import *
from helper import *
from thanks import *
from hello import *
from bye import *

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    user_message = req['request']['original_utterance'].lower()

    if req['session']['new'] and user_message == "":
        res['response']['text'] = authorization(user_id)
        logging.info("Authorising user")
        return

    if ('созд' in user_message or 'доб' in user_message) and \
            ('кошел' in user_message or 'счет' in user_message):
        res['response']['text'] = create_wallet(user_message, user_id)
        logging.info("Adding wallet")
        return

    if ('удал' in user_message or 'убр' in user_message) and \
            ('кошел' in user_message or 'счет' in user_message):
        res['response']['text'] = delete_wallet(user_message, user_id)
        logging.info("Deleting wallet")
        return

    if ('пополн' in user_message or 'зачисл' in user_message) and \
            ('кошел' in user_message or 'счет' in user_message):
        res['response']['text'] = "Пополнил кошелёк"
        logging.info("Adding money")
        return

    if ('трат' in user_message or 'сн' in user_message) and \
            ('кошел' in user_message or 'счет' in user_message):
        res['response']['text'] = "Снял с кошелька"
        logging.info("Spending money")
        return

    if ('выв' in user_message or 'дай' in user_message or 'ска' in user_message) and \
            'инф' in user_message and \
            ('кошел' in user_message or 'счет' in user_message):
        res['response']['text'] = "Вывел информацию о счёте"
        logging.info("Giving info about wallet")
        return

    if ('выв' in user_message or 'дай' in user_message or 'ска' in user_message) and \
            'стат' in user_message:
        res['response']['text'] = "Вывел статистику"
        logging.info("Giving statics about expenses")
        return

    if ('выв' in user_message or 'дай' in user_message
        or 'ска' in user_message or "покаж" in user_message
        or "показ" in user_message) and \
            ('кошел' in user_message or 'счет' in user_message):
        res['response']['text'] = return_wallets(user_id)
        logging.info("Giving all wallets")
        return

    if "помо" in user_message or ("что" in user_message and "ты" in user_message and "умеешь" in user_message):
        res['response']['text'] = helper()
        return

    if "спасибо" in user_message:
        res['response']['text'] = thanks()
        res['response']['end_session'] = True
        return

    if "привет" in user_message:
        res['response']['text'] = hello(req['session']['message_id'])
        return

    if "до свидания" in user_message or "пока" in user_message or "прощай" in user_message:
        res['response']['text'] = bye()
        return

    res['response']['text'] = "Извините, я Вас не понял."


if __name__ == '__main__':
    app.run(port=6000)

# cd C:\Users\Ярослав\OneDrive\Рабочий стол .\ngrok http 6000

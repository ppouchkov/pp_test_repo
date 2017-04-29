import os
import json
import logging
import requests

from tornado import web
from tornado.ioloop import IOLoop

TOKEN = '332923901:AAFZ2HhajHBTsH2a5w2lvadAIQfX2fWRB1A'


def convert_url_to_tinyurl(url):
    return requests.get('http://tinyurl.com/api-create.php?url={}'.format(url)).text


def set_webhook():
    requests.get('https://api.telegram.org/bot335133699:key/setWebhook?url={}'.format(
        'https://bort474-bot.herokuapp.com/bot335133699:key'))


def send_coordinates(chat_id, latitude, longitude, reply_to_message_id=None):
    data = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
    if reply_to_message_id:
        data['reply_to_message_id'] = reply_to_message_id
    requests.post(url='https://api.telegram.org/bot335133699:key/sendLocation',
                  data=data)


def send_message(chat_id, text, reply_to_message_id=None):
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    if reply_to_message_id:
        data['reply_to_message_id'] = reply_to_message_id
    requests.post(url='https://api.telegram.org/bot335133699:key/sendMessage',
                  data=data)


def process_request(json_request):
    if 'message' in json_request:
        message_id = json_request['message']['message_id']
        chat_id = json_request['message']['chat']['id']
        text = json_request['message'].get('text') or json_request['message'].get('caption')

        if text:
            send_message(chat_id, text, message_id)


# noinspection PyMethodOverriding
class SiteHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        if '335133699:key' in self.request.uri:
            try:
                json_data = json.loads(self.request.body.decode('utf8'))
                process_request(json_data)
            except ValueError:
                logging.exception('error in processing telegram message')


if __name__ == "__main__":
    set_webhook()
    app = web.Application([
        (r'.*', SiteHandler),
    ], )
    app.listen(int(os.environ.get("PORT", 5000)))
    IOLoop.current().start()
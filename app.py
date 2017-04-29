import telebot
from tornado.web import RequestHandler


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello from Tornado {}".format(self.__class__.__name__))


class BotHandler(RequestHandler):
    def initialize(self, bot):
        self.bot = bot

    def get(self):
        self.write("Hello from Tornado {}".format(self.__class__.__name__))

    def post(self):
        if ("Content-Length" in self.request.headers
                and "Content-Type" in self.request.headers
                and self.request.headers['Content-Type'] == "application/json"):

            # length = int(self.request.headers['Content-Length'])
            json_data = self.request.body.decode("utf-8")
            update = telebot.types.Update.de_json(json_data)
            self.bot.process_new_updates([update])
            self.write("")
            self.finish()
        else:
            self.write("What are you doing here?")

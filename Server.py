from flask import Flask, request
from QQBotTools.QQBot import QQBot


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.qqBot = QQBot(self.app)

        self._registerRoutes()

    def _registerRoutes(self):
        self._helloWorld()
        self._helloWorld2()

    def _helloWorld(self):
        @self.app.route('/', methods=["GET"])
        def _helloWorld():
            return "Hello World"

    def _helloWorld2(self):
        @self.app.route('/2', methods=["GET"])
        def _helloWorld2():
            return "Hello World2"


if __name__ == "__main__":
    server = Server()
    server.app.run(port=5555, host="0.0.0.0")

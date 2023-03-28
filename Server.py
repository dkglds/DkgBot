""" doc """
from flask import Flask, request
from QQBotTools.QQBot import QQBot


class Server(object):
    """ doc """

    def __init__(self, config_path):
        self.app = Flask(__name__)
        self.qq_bot = QQBot(self.app)

        self._register_routes()

    def _register_routes(self):
        self._hello_world()
        self._hello_world2()

    def _hello_world(self):
        @self.app.route('/', methods=["GET"])
        def _hello_world():
            """ doc """
            return "Hello World"

    def _hello_world2(self):
        @self.app.route('/2', methods=["GET"])
        def _hello_world2():
            """ doc """
            return "Hello World2"


if __name__ == "__main__":
    server = Server()
    server.app.run(port=5555, host="0.0.0.0")

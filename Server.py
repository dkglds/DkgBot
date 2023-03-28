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
        self.info_getting_server()

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

    def info_getting_server(self):
        @self.app.route('/', methods=["POST"])
        def info_getting_server():
            """
            从POST方式获取go-cphttp的网络信息
            :return:"ok"的返回信息
            """
            self.qq_bot.get_message_queueing(request.get_json())
            return "ok"


if __name__ == "__main__":
    server = Server()
    server.app.run(port=5555, host="0.0.0.0")

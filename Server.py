""" flask服务器类 """
from flask import Flask, request
from QQBotTools.QQBot import QQBot


class Server(object):
    """ flask服务器类 """

    def __init__(self):
        """
        初始化自身属性
        self.app: 实例flask服务器
        self.qq_bot: 实例一个qq机器人
        """
        self.app = Flask(__name__)
        self.qq_bot = QQBot()
        # 注册网页url
        self._register_routes()

    def _register_routes(self):
        """
        总注册方法，调用所有url注册方法
        :return: 无
        """
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
        """
        注册Post接口，从go-cphttp获取它接收到的信息
        :return:
        """
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

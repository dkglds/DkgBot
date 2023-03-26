from flask import Flask


class Server:
    def __init__(self):
        self.app = Flask(__name__)

        self._register_routes()

    def _register_routes(self):
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
    server.app.run()

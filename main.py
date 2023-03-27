from Server import Server

server = Server()
app = server.app

if __name__ == '__main__':
    app.run(port=5555, host="0.0.0.0")

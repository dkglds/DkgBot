""" doc """
from Server import Server
from Config import CONFIG

server = Server("resource/config.json")
app = server.app

if __name__ == '__main__':
    for i in CONFIG:
        print(CONFIG[i])
    app.run(port=5555, host="0.0.0.0")

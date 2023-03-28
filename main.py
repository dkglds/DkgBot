""" doc """
import Const
from Server import Server
from Config import CONFIG

server = Server("resource/config.json")
app = server.app

if __name__ == '__main__':
    '''
    for i in CONFIG:
        print(CONFIG[i])
    #'''
    app.run(port=CONFIG["qqbot"]["cqhttp_port"], host=Const.HTTP_INFO_GET_IP)

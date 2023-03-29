""" 主函数、服务启动配置 """
from Server import Server
from Config import Const
from Config.Config import CONFIG

server = Server()
app = server.app

if __name__ == '__main__':
    app.run(port=CONFIG["qq_bot"]["cqhttp_port"], host=Const.HTTP_INFO_GET_IP)

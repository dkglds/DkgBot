""" session工具类 """
import time
from copy import deepcopy
from Config.Roles import ROLES
from Config.Config import CONFIG


class SessionTools(object):
    """ session工具类 """

    def __init__(self, sessions=None):
        """
        初始化session字典
        :param sessions: 传入的session字典，不传入则新建立一个字典
        """
        if sessions is None:
            sessions = dict()
        self.sessions = sessions
        # session格式模板
        self.session_private_config = dict()
        self.session_group_config = dict()

    def reset_session_config(self):
        self.session_private_config = {
            'msg': ROLES[CONFIG["chatgpt"]["private_preset"]],
            'role': CONFIG["chatgpt"]["private_preset"],
            'last': 0,
            'id': "0"
        }
        self.session_group_config = {
            'msg': ROLES[CONFIG["chatgpt"]["group_preset"]],
            'role': CONFIG["chatgpt"]["group_preset"],
            'last': 0,
            'id': "0"
        }

    def get_chat_session(self, session_id):
        """
        根据给定id从字典获取用户的session，若没有则新建立个session
        :param session_id: 给定id
        :return: 给定id对应的session
        """
        if session_id not in self.sessions:
            self.reset_session_config()
            if session_id[0] == "G":
                config = deepcopy(self.session_group_config)
            else:
                config = deepcopy(self.session_private_config)
            config['last'] = time.time()
            config['id'] = session_id
            self.sessions[session_id] = config
        return self.sessions[session_id]

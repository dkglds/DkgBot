""" session工具类 """
from copy import deepcopy
from Config import CONFIG


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
        self.session_config = {
            'msg': [
                {"role": "system", "content": CONFIG["chatgpt"]["preset"]}
            ]
        }

    def get_chat_session(self, session_id):
        """
        根据给定id从字典获取用户的session，若没有则新建立个session
        :param session_id: 给定id
        :return: 给定id对应的session
        """
        if session_id not in self.sessions:
            config = deepcopy(self.session_config)
            config['id'] = session_id
            self.sessions[session_id] = config
        return self.sessions[session_id]

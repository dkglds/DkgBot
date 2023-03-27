""" doc """
from copy import deepcopy

import tiktoken


class SessionTools(object):
    """ doc """

    def __init__(self, sessions=None):
        if sessions is None:
            sessions = dict()
        self.sessions = sessions
        self.session_config = {
            'msg': [
                {"role": "system", "content": "待补充字符串"}
            ]
        }

    def get_chat_session(self, session_id):
        if session_id not in self.sessions:
            config = deepcopy(self.session_config)
            config['id'] = session_id
            self.sessions[session_id] = config
        return self.sessions[session_id]

    @staticmethod
    def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":
            num_tokens = 0
            for message in messages:
                num_tokens += 4
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # 如果name字段存在，role字段会被忽略
                        num_tokens += -1  # role字段是必填项，并且占用1token
            num_tokens += 2
            return num_tokens
        else:
            raise NotImplementedError(f"""当前模型不支持tokens计算: {model}.""")

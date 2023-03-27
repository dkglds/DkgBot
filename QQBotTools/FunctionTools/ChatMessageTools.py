from .OtherTools import OtherTools
from .SessionTools import SessionTools


class ChatMessageTools(object):
    """ doc """

    def __init__(self):
        # TODO document why this method is empty
        pass

    @staticmethod
    def chat_with_gpt(message, session):
        session['msg'].append({"role": "user", "content": message})
        # 检查是否超过tokens限制
        while SessionTools.num_tokens_from_messages(session['msg']) > 3000:
            # 当超过记忆保存最大量时，清理一条
            del session['msg'][2:3]
        # 与ChatGPT交互获得对话内容
        message = "假装ChatGpt返回的内容:" + str(message)
        # 记录上下文
        session['msg'].append({"role": "assistant", "content": message})
        '''
        print("ChatGPT返回内容: ")
        print(message)
        #'''
        print(session['msg'])
        return message

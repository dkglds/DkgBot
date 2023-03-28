""" doc """
from .OtherTools import OtherTools
from .SessionTools import SessionTools
from GPTTools.GPTTalker import GPTTalker


class ChatMessageTools(object):
    """ doc """
    with open("test_resource/_key.txt", "r") as f:
        key = [f.read()]
    talker = GPTTalker(key, "gpt-3.5-turbo")

    @classmethod
    def chat_with_gpt(cls, message, session):
        session['msg'].append({"role": "user", "content": message})
        # 检查是否超过tokens限制
        while SessionTools.num_tokens_from_messages(session['msg']) > 3000:
            # 当超过记忆保存最大量时，清理一条
            del session['msg'][2:3]
        # 与ChatGPT交互获得对话内容
        cls.talker.talk_with_gpt(session['msg'])
        message = cls.talker.return_str
        # 记录上下文
        session['msg'].append({"role": "assistant", "content": message})
        '''
        print("ChatGPT返回内容: ")
        print(message)
        #'''
        #print(session['msg'])
        return message

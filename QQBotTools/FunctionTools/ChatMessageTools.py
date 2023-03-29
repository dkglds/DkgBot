""" GPT信息传递类方法集合 """
import tiktoken
from GPTTools.GPTTalker import GPTTalker
from Config.Config import CONFIG
from QQBotTools.FunctionTools.OtherTools import get_bj_time


class ChatMessageTools(object):
    """ 与GPT信息传递有关的类 """
    key = CONFIG["openai"]["api_key"]
    talker = GPTTalker(key, CONFIG["chatgpt"]["model"])

    @classmethod
    def chat_with_gpt(cls, message, session):
        """
        对发送消息进行判别和处理后调用GPTTalker类的talk_with_gpt接口函数
        :param message: 将发送信息
        :param session: 用户的session
        :return: GPT回复的信息
        """
        session['msg'][1] = {"role": "user", "content": "current time:" + get_bj_time()}
        session['msg'].append({"role": "user", "content": message})
        # 检查是否超过tokens限制
        while cls.num_tokens_from_messages(session['msg']) > 3000:
            # 当超过记忆保存最大量时，清理一条
            session['msg'].pop(4)
        # 与ChatGPT交互获得对话内容
        cls.talker.talk_with_gpt(session['msg'])
        message = cls.talker.return_str
        # 记录上下文
        session['msg'].append({"role": "assistant", "content": message})
        '''
        print("ChatGPT返回内容: ")
        print(message)
        #'''
        # print(session['msg'])
        return message

    @classmethod
    def chat_with_gpt_by_new_log(cls, session):
        """
        清空消息记忆并且发起一个新话题
        :param session: 用户的session
        :return: GPT回复的信息
        """
        session['msg'][1] = {"role": "user", "content": "current time:" + get_bj_time()}
        session['msg'] = session["msg"][0:4]
        session["msg"].append({"role": "system", "content": "随便说点"})
        # 与ChatGPT交互获得对话内容
        cls.talker.talk_with_gpt(session["msg"])
        message = cls.talker.return_str
        # 记录上下文
        session['msg'].append({"role": "assistant", "content": message})
        # print(session['msg'])
        return message

    @staticmethod
    def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
        """
        根据使用的模型，计算一组信息的token量
        :param messages: 待计算信息
        :param model: 使用的模型
        :return: 信息的token量
        """
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

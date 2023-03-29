""" GPTTaker类 """
#import GPTTools.MyOpenAi as openai
import openai
from Config import Const


class GPTTalker(object):
    """
    GPT交谈者，
    用key列表和所选模型字符串构建对象
    调用talkWithGPT传入待分析信息后返回gpt是否回复成功的bool值
    调用函数后，回复的信息保存在self.returnStr中
    """

    def __init__(self, apl_keys_list, model):
        """
        :param apl_keys_list: key列表
        :param model: 所选模型
        """
        self.api_keys_list = apl_keys_list
        self.model = model
        self.max_key_list_len = len(apl_keys_list)
        self.current_key = 0
        self.return_str = str()

    def _check_keys(self):
        """
        对key列表和当前所选key检查
        :return: 是否成功通过检查的bool值，未通过的原因保存在self.returnStr中
        """
        if not self.api_keys_list:
            self.return_str = "请设置Api Key"
            return Const.FAILING
        elif self.current_key > self.max_key_list_len:
            self.current_key = 0
            self.return_str = "全部Key均已达到速率限制,请等待一分钟后再尝试"
            return Const.FAILING
        return Const.SUCCESS

    def _get_response_from_messages(self, messages):
        """
        从消息列表中获取回答
        :param messages: 待传入消息列表
        :return: 成功结果，回复内容保存在self.returnStr中
        """
        openai.api_key = self.api_keys_list[self.current_key]
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        self.return_str = resp['choices'][0]['message']['content']
        return Const.SUCCESS

    def _exception_handling(self, exception):
        """
        异常处理，根据部分预设异常进行处理
        :param exception: 传入的异常
        :return: 处理的异常是否是预设好的异常的bool，不是则将异常保存在self.returnStr中
        """
        if str(exception).__contains__(
                "Rate limit reached for default-gpt-3.5-turbo"
        ):
            # 切换key
            self.current_key += 1
            print("速率限制，尝试切换key")
            return Const.SUCCESS
        elif str(exception).__contains__(
                "Your access was terminated due to violation of our policies"
        ):
            """
            注意：这里未来可以设计为向机器人管理员发送key异常的信息，现在暂时维持现状
            """
            print("\n请及时确认该Key: \n" + str(openai.api_key) + "\n是否正常，若异常，请移除\n")
            print("访问被阻止，尝试切换Key")
            self.current_key += 1
            return Const.SUCCESS
        else:
            print('openai 接口报错: ' + str(exception))
            self.return_str = 'openai 接口报错: ' + str(exception)
            return Const.FAILING

    def talk_with_gpt(self, messages):
        """
        主接口函数，按照逻辑调用方法与GPT交互
        :param messages: 传入的信息列表
        :return: 是否成功回答的bool值，回答的信息、错误原因保存在returnStr中
        """
        test_time = 0
        while test_time < 5:
            try:
                if self._check_keys() == Const.FAILING:
                    return Const.FAILING
                if self._get_response_from_messages(messages) == Const.SUCCESS:
                    return Const.SUCCESS
            except openai.OpenAIError as exception:
                if self._exception_handling(exception) == Const.SUCCESS:
                    test_time += 1
                    continue
                else:
                    return Const.FAILING


if __name__ == "__main__":
    with open(r"C:\Users\86188\Documents\GitHub\DkgBot\resource\_key.txt", "r") as f:
        key = f.read()
    a = GPTTalker([key], "gpt-3.5-turbo")
    a.talk_with_gpt([{'role': 'user', 'content': '我正在测试api是否调用正常,请回答：“你好”'}])
    print(a.return_str)

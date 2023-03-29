""" 指令处理类 """
import Const


class InstructionProcessingTool(object):
    """ 指令处理类，可以通过继承重写process_instruction方法实现自定义指令 """

    def __init__(self, session_tool):
        """
        :param session_tool: 待获取的session
        """
        self.session_tool = session_tool
        self.message_json = None
        self.return_str = ""

    def process_instruction(self, message_json):
        """
        对输入的消息处理。
        如果它符合某个指令，则将消息处理后返回成功处理的信息
        不符合任何一条指令格式，则返回失败信息，进行默认的回复处理
        :param message_json: 输入的信息内容
        :return: 成功/失败
        """
        self.message_json = message_json
        message = message_json.get('raw_message')
        uid = message_json.get('sender').get('user_id')
        return Const.FAILING

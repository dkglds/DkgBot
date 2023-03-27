""" doc """
import Const
from QQBotTools.InstructionProcessingTool import InstructionProcessingTool
from QQBotTools.FunctionTools.ChatMessageTools import ChatMessageTools


class IntegratedInformationProcessingTool(object):
    """ doc """

    def __init__(self, session_tool):
        self.session_tool = session_tool
        self.instruction_processing_tool = InstructionProcessingTool(session_tool)
        self.uid = None
        self.message = None
        self.sender = None
        self.message_json = None

    def _read_partial_information(self, message_json):
        self.message_json = message_json
        # 消息发送者的资料
        self.sender = self.message_json.get('sender')
        # 消息类型
        self.message_type = self.message_json.get('message_type')
        # 获取原始信息
        self.message = self.message_json.get('raw_message')
        # 获取信息发送者的 QQ号码
        if self.sender is not None:
            self.uid = self.sender.get('user_id')

    def processing(self, message_json):
        self._read_partial_information(message_json)
        if self.message_type == "private":
            print("收到私聊消息：")
            print(self.message)
            session = self.session_tool.get_chat_session("P" + str(self.uid))
            if self.instruction_processing_tool.process_instruction(message_json) == Const.SUCCESS:
                return ""
            else:
                return ChatMessageTools.chat_with_gpt(self.message, session)
        return ""
'''
        print(self.uid)
        print(self.sender)
        print(self.message_type)
        print(self.message)
'''
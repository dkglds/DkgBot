""" 综合信息处理类，若想自定义消息收发逻辑，可以继承此类添加需要识别的更多信息与处理逻辑 """
from QQBotTools.ClassTools.InstructionProcessingTool import InstructionProcessingTool
from QQBotTools.FunctionTools.ChatMessageTools import ChatMessageTools
from QQBotTools.ClassTools.InformationSender import InformationSender
from QQBotTools.FunctionTools.OtherTools import read_partial_information
from Config import Const
from Config.Config import CONFIG


class IntegratedInformationProcessingTool(object):
    """ 综合信息处理类 """

    def __init__(self, session_tool):
        """
        获取session字典
        :param session_tool: 提供的session字典
        """
        self.sender = None
        self.uid = None
        self.message = None
        self.message_type = None
        self.session_tool = session_tool
        self.instruction_processing_tool = InstructionProcessingTool(session_tool)
        self.qq_no = CONFIG["qq_bot"]["qq_no"]

    def processing(self, message_json):
        """
        信息处理逻辑
        :param message_json: 收到的目标信息报文
        :return: 根据报文内的各种信息，回复的信息内容
        """
        read_partial_information(self, message_json)
        return_message = "1"
        if self.message_type == "private":
            print("收到私聊消息：")
            print(self.message)
            session = self.session_tool.get_chat_session("P" + str(self.uid))
            if self.instruction_processing_tool.process_instruction(message_json) == Const.SUCCESS:
                return_message = self.instruction_processing_tool.return_str
            else:
                return_message = ChatMessageTools.chat_with_gpt(self.message, session)
            InformationSender.send_private_message(self.uid, return_message, False)
        if self.message_type == 'group':  # 如果是群消息
            # 判断当被@时才回答
            if str("[CQ:at,qq=%s]" % self.qq_no) in self.message:
                gid = message_json.get('group_id')  # 群号
                print("收到群聊消息：")
                print(self.message)
                message = str(self.message).replace(str("[CQ:at,qq=%s]" % self.qq_no), '')
                session = self.session_tool.get_chat_session('G' + str(gid))
                if self.instruction_processing_tool.process_instruction(message_json) == Const.SUCCESS:
                    return_message = self.instruction_processing_tool.return_str
                else:
                    return_message = ChatMessageTools.chat_with_gpt(self.message, session)
                InformationSender.send_group_message(gid, return_message, self.uid, False)
        return return_message

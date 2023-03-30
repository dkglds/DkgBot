""" 综合信息处理类，若想自定义消息收发逻辑，可以继承此类添加需要识别的更多信息与处理逻辑 """
import random

from QQBotTools.ClassTools.InstructionProcessingTool import InstructionProcessingTool
from QQBotTools.FunctionTools.ChatMessageTools import ChatMessageTools
from QQBotTools.ClassTools.InformationSender import InformationSender
from QQBotTools.FunctionTools.OtherTools import read_partial_information
from Config import Const
from Config.Config import CONFIG

CQ_AT = "[CQ:at,qq=%s]"


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
        self.message_json = None
        self.session_tool = session_tool
        self.instruction_processing_tool = InstructionProcessingTool(session_tool)
        self.qq_no = CONFIG["qq_bot"]["qq_no"]

    def _processing_private(self):
        """
        私聊信息处理
        :return: 最后发送的消息
        """
        if self.uid in CONFIG["chat_in_qq"]["serve_privates_list"]:
            print("收到私聊消息：")
            print(self.message)
            session = self.session_tool.get_chat_session("P" + str(self.uid))
            if self.instruction_processing_tool.process_instruction(self.message_json) == Const.SUCCESS:
                return_message = self.instruction_processing_tool.return_str
            elif self.uid != CONFIG["qq_bot"]["qq_no"]:
                return_message = ChatMessageTools.chat_with_gpt(self.message, session)
            else:
                return_message = ""
            InformationSender.send_private_message(self.uid, return_message, False)
            return return_message
        else:
            return ""

    def _processing_group(self):
        """
        群聊消息处理
        :return: 最后发送的消息
        """
        gid = self.message_json.get('group_id')  # 群号
        message_id = self.message_json.get("message_id")
        return_message = ""
        if str(CQ_AT % self.qq_no) in self.message and gid in CONFIG["chat_in_qq"]["serve_groups_list"]:
            print("收到群聊消息：")
            print(self.message)
            self.message = str(self.message).replace(str(CQ_AT % self.qq_no), '')
            session = self.session_tool.get_chat_session('G' + str(gid))
            if self.instruction_processing_tool.process_instruction(self.message_json) == Const.SUCCESS:
                return_message = self.instruction_processing_tool.return_str
            elif self.uid != CONFIG["qq_bot"]["qq_no"]:
                return_message = ChatMessageTools.chat_with_gpt(self.message, session)
            else:
                return_message = ""
            InformationSender.send_group_message(gid, return_message, self.uid, False, message_id)
        elif CONFIG["random_response"]["on"]:
            return_message = self.reply_message_randomly()
        return return_message

    def processing(self, message_json):
        """
        信息处理逻辑
        :param message_json: 收到的目标信息报文
        :return: 根据报文内的各种信息，回复的信息内容
        """
        self.message_json = message_json
        read_partial_information(self, message_json)
        if self.message_type == "private":
            return_message = self._processing_private()
        elif self.message_type == 'group':  # 如果是群消息
            return_message = self._processing_group()
        else:
            return_message = self.message_type
        return return_message

    @staticmethod
    def send_new_log(session):
        """
        向目标发起新对话
        :param session: 目标的session
        :return: 发送的消息
        """
        message = ChatMessageTools.chat_with_gpt_by_new_log(session)
        if session["id"][0] == "G":
            gid = int(session["id"].replace("G", ""))
            InformationSender.send_group_message(gid, message, None, False, None)
        else:
            uid = int(session["id"].replace("P", ""))
            InformationSender.send_private_message(uid, message, False)
        return message

    def reply_message_randomly(self):
        """
        随机回复群对话
        :return: 回复的消息
        """
        gid = self.message_json.get('group_id')
        message_id = self.message_json.get("message_id")
        return_message = ""
        if gid in CONFIG["random_response"]["serve_groups_list"] and \
                random.random() < CONFIG["random_push"]["reply_probability"]:
            self.message = str(self.message).replace(str(CQ_AT % self.qq_no), '')
            session = self.session_tool.get_chat_session('G' + str(gid))
            if self.instruction_processing_tool.process_instruction(self.message_json) == Const.SUCCESS:
                return_message = self.instruction_processing_tool.return_str
            elif self.uid != CONFIG["qq_bot"]["qq_no"]:
                return_message = ChatMessageTools.chat_with_gpt(self.message, session)
            else:
                return_message = ""
            InformationSender.send_group_message(gid, return_message, self.uid, False, message_id)
        return return_message

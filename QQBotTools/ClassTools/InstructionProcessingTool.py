""" 指令处理类 """
from Config import Const
from Config.Config import CONFIG
from QQBotTools.FunctionTools.OtherTools import read_partial_information
from Config.Roles import ROLES
from QQBotTools.FunctionTools.OtherTools import get_credit_summary_by_index

CQ_AT = "[CQ:at,qq=%s]"


class InstructionProcessingTool(object):
    """ 指令处理类，可以通过继承重写process_instruction方法实现自定义指令 """

    def __init__(self, session_tool):
        """
        :param session_tool: 待获取的session
        """
        self.session_tool = session_tool
        self.admin_list = CONFIG["qq_bot"]["admin_qq"]
        self.sender = None
        self.uid = None
        self.message = None
        self.message_type = None
        self.return_str = ""
        self.qq_no = CONFIG["qq_bot"]["qq_no"]

    def process_instruction(self, message_json):
        """
        对输入的消息处理。
        如果它符合某个指令，则将消息处理后返回成功处理的信息
        不符合任何一条指令格式，则返回失败信息，进行默认的回复处理
        :param message_json: 输入的信息内容
        :return: 成功/失败
        """
        read_partial_information(self, message_json)
        self.message = message_json.get('raw_message')
        self.uid = message_json.get('sender').get('user_id')
        self.message = str(self.message).replace(str(CQ_AT % self.qq_no), '')
        if "#" == self.message.strip()[0]:
            message = self.message.replace("#", "", 1).strip()
            if hasattr(self, message.split("(")[0]):
                if self.message_type == "group" and self.uid not in self.admin_list:
                    self.return_str = "权限不足！"
                    return Const.SUCCESS
                # exec("self." + message)
                try:
                    if message[-1] != ")":
                        message += "()"
                    exec("self." + message)
                except Exception as error:
                    self.return_str = "异常:" + str(error)
            else:
                self.return_str = "指令错误！\n你可以使用：“#help()”来查询支持的指令集。"
            return Const.SUCCESS
        return Const.FAILING

    def reset(self):
        """
        重置对话
        :return: 是否处理成功
        """
        if self.message_type == 'group':
            session_id = "G" + str(self.uid)
        elif self.message_type == 'private':
            session_id = "P" + str(self.uid)
        else:
            self.return_str = "尚未设置处理此消息的功能"
            return Const.FAILING
        session = self.session_tool.get_chat_session(session_id)
        session["msg"] = ROLES[int(session["role"])]
        self.return_str = "会话已重置"
        return Const.SUCCESS

    def change_role(self, role_no=0):
        """
        切换人格
        :return: 是否处理成功
        """
        if role_no >= len(ROLES):
            self.return_str = "没有这个人格，请输入0~" + str(len(ROLES) - 1) + "间的数"
            return Const.FAILING
        if self.message_type == 'group':
            session_id = "G" + str(self.uid)
        elif self.message_type == 'private':
            session_id = "P" + str(self.uid)
        else:
            self.return_str = "尚未设置处理此消息的功能"
            return Const.FAILING
        session = self.session_tool.get_chat_session(session_id)
        session["role"] = int(role_no)
        session["msg"] = ROLES[session["role"]]
        self.return_str = "已切换为人格" + str(role_no)
        return Const.SUCCESS

    def check_balance(self):
        """
        查询余额
        :return: 是否处理成功
        """
        text = ""
        for i in range(len(CONFIG['openai']['api_key'])):
            text = text + "Key_" + str(i + 1) + " 余额: " + str(round(get_credit_summary_by_index(i), 2)) + "美元\n"
        self.return_str = text[0:len(text) - 1]
        return Const.SUCCESS

    def help(self):
        """
        打印指令集
        :return: 是否处理成功
        """
        self.return_str = \
            "#reset() : 重置对话\n" + \
            "#change_role(编号) : 切换人格\n" + \
            "#check_balance() : 查询余额"
        return Const.SUCCESS

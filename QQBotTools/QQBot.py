""" QQ机器人类 """
import time

from threading import Thread
from QQBotTools.IntegratedInformationProcessingTool import IntegratedInformationProcessingTool
from QQBotTools.ClassTools.SessionTools import SessionTools
from QQBotTools.LogicalProcessingThread import LogicalProcessingThread
from Config.Config import CONFIG

class QQBot(object):
    """ QQ机器人类 """

    def __init__(self,
                 logical_processing_thread=LogicalProcessingThread,
                 processing_tool=IntegratedInformationProcessingTool
    ):
        """
        初始化，需要提供一个综合消息处理器的类，不提供则使用默认的处理器
        :param logical_processing_thread: 逻辑处理器类
        """
        self.get_message_queue = list()
        self.send_message_queue = list()
        self.session_tool = SessionTools()
        self._init_sessions()
        # 根据给定的综合信息处理类实例化一个对象
        self.logical_processing_tool = logical_processing_thread(
            self.session_tool,
            self.get_message_queue,
            processing_tool
        )
        self.logical_processing_thread = Thread(target=self.logical_processing_tool.run_thread)
        self._active_thread()

    def _init_sessions(self):
        for each_private_id in CONFIG["random_push"]["serve_privates_list"]:
            self.session_tool.get_chat_session("P" + str(each_private_id))
        for each_group_id in CONFIG["random_push"]["serve_groups_list"]:
            self.session_tool.get_chat_session("G" + str(each_group_id))

    def _active_thread(self):
        """
        处理线程
        :return: 无
        """
        print("线程启动")
        self.logical_processing_thread.start()

    def get_message_queueing(self, get_message):
        """
        消息入队列
        :param get_message: 目标消息报文
        :return: 将目标消息加入队列尾
        """
        self.get_message_queue.append(get_message)

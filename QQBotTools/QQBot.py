""" QQ机器人类 """
import time

from threading import Thread
from QQBotTools.IntegratedInformationProcessingTool import IntegratedInformationProcessingTool
from QQBotTools.ClassTools.SessionTools import SessionTools


class QQBot(object):
    """ QQ机器人类 """

    def __init__(self, processing_tool=IntegratedInformationProcessingTool):
        """
        初始化，需要提供一个综合消息处理器的类，不提供则使用默认的处理器
        :param processing_tool: 综合信息处理器类
        """
        self.get_message_queue = list()
        self.send_message_queue = list()
        self.session_tool = SessionTools()
        # 根据给定的综合信息处理类实例化一个对象
        self.integrated_information_processing_tool = processing_tool(self.session_tool)
        self.information_processing_thread = Thread(target=self.information_processing_thread_work)
        self._active_thread()

    def _active_thread(self):
        """
        启动信息读取线程
        :return: 无
        """
        print("线程启动")
        self.information_processing_thread.start()

    def information_processing_thread_work(self):
        """
        信息读取线程的运行
        具体为反复检测消息队列中的是否有信息，有信息则取第一条调用综合信息处理器处理，否则等0.05秒后检测
        :return: 打印回复的内容
        """
        while True:
            if len(self.get_message_queue) == 0:
                time.sleep(0.05)
                continue
            print("回复：")
            print(self.integrated_information_processing_tool.processing(self.get_message_queue.pop(0)))

    def get_message_queueing(self, get_message):
        """
        消息入队列
        :param get_message: 目标消息报文
        :return: 将目标消息加入队列尾
        """
        self.get_message_queue.append(get_message)

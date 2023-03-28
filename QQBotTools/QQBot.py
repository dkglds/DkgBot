""" doc """
import time

from threading import Thread
from QQBotTools.IntegratedInformationProcessingTool import IntegratedInformationProcessingTool
from QQBotTools.FunctionTools.SessionTools import SessionTools


class QQBot(object):
    """ doc """

    def __init__(self, server, processing_tool=IntegratedInformationProcessingTool):
        self.server = server
        self.get_message_queue = list()
        self.send_message_queue = list()
        self.session_tool = SessionTools()
        self.integrated_information_processing_tool = processing_tool(self.session_tool)
        self.information_processing_thread = Thread(target=self.information_processing_thread_work)
        self._active_thread()

    def _active_thread(self):
        print("线程启动")
        self.information_processing_thread.start()

    def information_processing_thread_work(self):
        while True:
            if len(self.get_message_queue) == 0:
                time.sleep(0.05)
                continue
            print("回复：")
            print(self.integrated_information_processing_tool.processing(self.get_message_queue.pop(0)))

    def get_message_queueing(self, get_message):
        self.get_message_queue.append(get_message)

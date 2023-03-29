""" doc """
import time
import schedule
import random

from QQBotTools.IntegratedInformationProcessingTool import IntegratedInformationProcessingTool
from QQBotTools.FunctionTools.OtherTools import get_bj_time
from Config.Config import CONFIG

class LogicalProcessingThread(object):
    """ doc """

    def __init__(self, session_tool, message_queue, processing_tool=IntegratedInformationProcessingTool):
        self.session_tool = session_tool
        self.message_queue = message_queue
        self.processing_tool = processing_tool(self.session_tool)
        self.running = True
        if CONFIG["qq_bot"]["random_push"]:
            schedule.every(10).seconds.do(self.send_message_randomly_to_all)

    def process_message(self):
        message = self.message_queue.pop(0)
        session = self.get_session_from_message(message)
        if session is not None:
            print(self.processing_tool.processing(message))
            session["last"] = time.time()

    def get_session_from_message(self, message):
        message_type = message.get('message_type')
        if message_type == "private":
            uid = message.get('sender').get('user_id')
            session = self.session_tool.get_chat_session("P" + str(uid))
        elif message_type == "group":
            gid = message.get('group_id')
            session = self.session_tool.get_chat_session("G" + str(gid))
        else:
            session = None
        return session

    def logic(self):
        schedule.run_pending()
        if len(self.message_queue) == 0:
            time.sleep(0.1)
            return
        print("回复：")
        self.process_message()

    def send_message_randomly(self, session):
        if time.time() - session["last"] >= 600:
            session["msg"] = session["msg"][0:4]
            current_time = get_bj_time().split(" ")[1].split(":")[0]
            #if int(current_time) >= 7 and random.random() < 0.003:
            if random.random() < 0.003:
                message = self.processing_tool.send_new_log(session)
                print("发出：")
                print(message)

    def send_message_randomly_to_all(self):
        for each_session in self.session_tool.sessions:
            self.send_message_randomly(self.session_tool.sessions[each_session])
        print(self.session_tool.sessions.keys())

    def run_thread(self):
        while True:
            self.logic()

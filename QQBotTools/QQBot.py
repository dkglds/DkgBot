import time

from flask import request
from threading import Thread


class QQBot:
    def __init__(self, server):
        self.server = server
        self.messageQueue = list()
        self.informationProcessingThread = Thread(target=self.informationProcessingThreadWork)
        self._registerRoutes()
        self._activeThread()

    def _activeThread(self):
        print("线程启动")
        self.informationProcessingThread.start()

    def informationProcessingThreadWork(self):
        while True:
            if len(self.messageQueue) == 0:
                time.sleep(0.05)
                continue
            self._IntegratedInformationProcessing(self.messageQueue.pop(0))

    def _IntegratedInformationProcessing(self,message):
        print(message)
        pass

    def _registerRoutes(self):
        self.infoGetingServer()
        pass

    def infoGetingServer(self):
        @self.server.route('/', methods=["POST"])
        def infoGetingServer():
            self.messageQueue.append(request.get_json())
            #print(self.messageQueue)
            return "ok"

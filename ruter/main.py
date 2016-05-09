# -*- coding: utf-8 -*-


import os
import sys
import signal
import time

import ruter.api
from ruter.status_printer import StatusPrinter


class Main(ruter.api.Customer):
    def __init__(self):
        self.__args = sys.argv[1:]
        self.__status = StatusPrinter()
        self.__performer = ruter.api.SimplePerformer()
        self.__performer.attach(self)
        signal.signal(signal.SIGINT, self.on_signal)
    
    def on_signal(self, signum, frame):
        self.__performer.stop()

    def update(self, sender, task):
        if isinstance(task, ruter.api.GetStopsRuterTask):
            i = 0
            for stop in task.state:
                i += 1
                sender.submit(ruter.api.GetStopTask(stop["ID"]))
                if i > 20:
                    break
            sender.stop()
        print("update: {0}".format(type(task).__name__))

    def main(self):
        start = time.time()
        self.__status.message("Using Ruter ReisAPI")
        #get_stops_ruter = ruter.api.GetStopsRuterTask()
        #self.__performer.submit(get_stops_ruter)
        #rc = self.__performer.start(16)
        for i in range(0, 100):
            self.__performer.submit(ruter.api.SleepTask())
        self.__performer.stop()
        rc = self.__performer.start(32)
        print("Duration: {0}".format(time.time() - start))
        return rc


#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

# Standard
import queue
import signal
import threading

# Local
import interfaces


class ApiBus(interfaces.ISubject):
    def __init__(self, threads=3):
        self.__completed_commands = queue.Queue()
        self.__enabled = True
        self.__observers = set()
        self.__pending_commands = queue.Queue()
        self.__threads = [
            threading.Thread(target=self.__thread_main, daemon=True)
            for i in range(0, threads)
        ]
    def stop(self):
        self.__threads.join()
        self.__enabled = False
    def pump(self):
        [thread.start() for thread in self.__threads]
        while self.__enabled:
            command = self.__completed_commands.get(True)
            self.notify(command)
    def request(self, command):
        self.__pending_commands.put(command)
    def attach(self, observer):
        self.__observers.add(observer)
    def detach(self, observer):
        self.__observers.discard(observer)
    def notify(self, command):
        for observer in self.__observers:
            observer.update(command)
    def __thread_main(self):
        #signal.signal(signal.SIGINT, signal.SIG_IGN)
        while self.__enabled:
            command = self.__pending_commands.get(True)
            command.execute()
            self.__completed_commands.put(command)
        print("Process terminating...")

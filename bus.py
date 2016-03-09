#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

# Standard
import multiprocessing

# Local
import interfaces


class ApiBus(interfaces.ISubject):
    def __init__(self):
        self.__observers = set()
        self.__commands = multiprocessing.Queue()
        self.__pool = multiprocessing.Pool(processes=3,
                                           initializer=self.__worker_main,
                                           initargs=(self.__commands,),
                                           maxtasksperchild=None)
    def request(self, command):
        self.__commands.put(command)
    def attach(self, observer):
        self.__observers.add(observer)
    def detach(self, observer):
        self.__observers.discard(observer)
    def notify(self, command):
        map(lambda x:x.update(command), self.__observers)
    def __worker_main(self, queue):
        while True:
            command = queue.get(True)
            command.execute()
            self.notify(command)

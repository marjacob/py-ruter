#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

# Standard
import multiprocessing

# Local
import interfaces


class ApiBus(interfaces.ISubject):
    def __init__(self):
        self.__completed_commands = multiprocessing.Queue()
        self.__enabled = True
        self.__observers = set()
        self.__pending_commands = multiprocessing.Queue()
        self.__thread_pool = multiprocessing.Pool(
            processes=3,
            initializer=self.__worker_main,
            initargs=(self.__pending_commands,),
            maxtasksperchild=None)

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError()
        else:
            self.__enabled = value

    def pump(self):
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
    def __worker_main(self, queue):
        while self.__enabled:
            command = queue.get(True)
            command.execute()
            self.__completed_commands.put(command)

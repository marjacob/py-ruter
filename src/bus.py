#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

# Standard
import queue
import signal
import threading

# Local
import interfaces


class ApiBus(interfaces.ISubject):
    """
    The central bus which forwards incoming API requests and makes the result
    available for consumption by multiple consumers.
    """

    def __init__(self, threads=3):
        self.__active_threads = 0
        self.__completed_commands = queue.Queue()
        self.__enabled = True
        self.__observers = set()
        self.__pending_commands = queue.Queue()
        self.__threads = [
            threading.Thread(target=self.__thread_main, daemon=False)
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
        self.__active_threads += 1
        while self.__enabled:
            command = self.__pending_commands.get(True)

            if isinstance(command, AbortCommand):
                self.__active_threads -= 1
                self.__enabled = False
                self.__pending_commands.put(command)

                # Post the completed abort if this was the last thread.
                if self.__active_threads == 0:
                    self.__completed_commands.put(command)
            else:
                command.execute()
                self.__completed_commands.put(command)


class AbortCommand(interfaces.ICommand):
    """
    A special command which causes an ApiBus to exit as fast as possible, but
    without aborting previously queued requests.
    """

    def __init__(self, exit_code):
        self.__exit_code = exit_code
    def execute(self):
        return self.__exit_code
    @property
    def result(self):
        return self.__exit_code

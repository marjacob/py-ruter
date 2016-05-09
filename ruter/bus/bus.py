#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

# Standard
import queue
import signal
import threading

# Local
import bus


class CommandBus(bus.ISubject):
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

    def stop(self, exit_code=0):
        """
        Request that all threads terminate after completing their work.
        """
        self.request(AbortCommand(exit_code))

    def pump(self):
        """
        Process commands until terminated.
        """
        # Start worker threads.
        for thread in self.__threads:
            thread.start()
        # Notify subscribers when a command completes.
        while self.__enabled:
            command = self.__completed_commands.get(True)
            self.notify(command)

    def request(self, command):
        """
        Queue a command for processing by a worker thread.
        """
        self.__pending_commands.put(command)

    def attach(self, observer):
        """
        Listen to completed commands.
        """
        self.__observers.add(observer)

    def detach(self, observer):
        """
        Stop listening to completed commands.
        """
        self.__observers.discard(observer)

    def notify(self, command):
        """
        Notify all listeners of a completed command.
        """
        for observer in self.__observers:
            observer.update(command)

    def __thread_main(self):
        """
        Worker threads start executing from here.
        """
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


class AbortCommand(bus.ICommand):
    """
    A special command which causes an CommandBus to exit as fast as possible,
    but without aborting previously queued requests.
    """

    def __init__(self, exit_code):
        self.__exit_code = exit_code
    def __repr__(self):
        return "{0}({1})".format(type(self).__name__, self.__exit_code)
    def __str__(self):
        return "abort({0})".format(self.__exit_code)
    def execute(self):
        """
        Returns the exit code.
        """
        return self.__exit_code
    @property
    def result(self):
        """
        Returns the exit code.
        """
        return self.__exit_code

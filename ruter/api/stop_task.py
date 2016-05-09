# -*- coding: utf-8 -*-


import os

from ruter.api.task import Task


class StopTask(Task):
    def __init__(self, threads, exit_code=None):
        self.__exit_code = exit_code if exit_code else os.EX_OK
        self.__threads = threads

    def execute(self):
        self.__threads -= 1
        return self.__threads > 0

    @property
    def state(self):
        return self.__exit_code

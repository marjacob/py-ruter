# -*- coding: utf-8 -*-


import time

from ruter.api.task import Task


class SleepTask(Task):
    def __init__(self, delay=5):
        self.__delay = delay

    def execute(self):
        time.sleep(self.__delay)
        return True

    def state(self):
        return None



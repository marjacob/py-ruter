# -*- coding: utf-8 -*-


class StopTask(Task):
    def __init__(self, exit_code=None):
        self.__exit_code = exit_code if exit_code else os.EX_OK
    def execute(self):
        pass
    @property
    def state(self):
        return self.__exit_code

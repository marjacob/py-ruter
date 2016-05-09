# -*- coding: utf-8 -*-


import abc


class Task(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass
    @abc.abstractproperty
    def state(self):
        pass

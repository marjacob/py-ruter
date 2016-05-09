# -*- coding: utf-8 -*-


import abc


class Handler(abc.ABC):
    @abc.abstractmethod
    def handle(self, task):
        pass


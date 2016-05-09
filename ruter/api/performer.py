# -*- coding: utf-8 -*-


import abc


class Performer(abc.ABC):
    @abc.abstractmethod
    def attach(self, customer):
        pass
    @abc.abstractmethod
    def detach(self, customer):
        pass
    @abc.abstractmethod
    def start(self, threads=3):
        pass
    @abc.abstractmethod
    def stop(self, exit_code=None):
        pass
    @abc.abstractmethod
    def submit(self, task):
        pass

# -*- coding: utf-8 -*-


import abc


class Customer(abc.ABC):
    @abc.abstractmethod
    def update(self, sender, task):
        pass

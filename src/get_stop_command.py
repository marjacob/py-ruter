#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

import interfaces
import ruter


class GetStopCommand(interfaces.ICommand):
    def __init__(self, stop_id):
        self.__result = None
        self.__stop_id = stop_id
    @property
    def result(self):
        return self.__result
    def execute(self):
        self.__result = ruter.Stop.from_id(self.__stop_id)

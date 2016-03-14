#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

import interfaces
import ruter


class GetDeparturesCommand(interfaces.ICommand):
    def __init__(self, stop_id, time=None):
        self.__result = None
        self.__stop_id = stop_id
        self.__time = time
    def execute(self):
        self.__result = ruter.Departure.from_stop_id(self.__stop_id,
                                                     self.__time)
    @property
    def result(self):
        return self.__result

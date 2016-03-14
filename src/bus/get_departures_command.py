#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

from bus import interfaces
import ruter


class GetDeparturesCommand(interfaces.ICommand):
    def __init__(self, stop_id, time=None):
        self.__result = None
        self.__stop_id = stop_id
        self.__time = time
    def __repr__(self):
        return "{0}({1}, {2})".format(
            type(self).__name__,
            self.__stop_id,
            self.__time)
    def __str__(self):
        return "get_departures(stop_id={0}, time={1})".format(self.__stop_id, self.__time)
    def execute(self):
        self.__result = ruter.Departure.from_stop_id(self.__stop_id,
                                                     self.__time)
    @property
    def result(self):
        return self.__result

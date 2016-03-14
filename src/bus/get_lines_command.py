#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

from bus import interfaces
import ruter


class GetLinesCommand(interfaces.ICommand):
    def __init__(self, stop_id):
        self.__result = None
        self.__stop_id = stop_id

    def __repr__(self):
        return "{0}({1})".format(type(self).__name__, self.__stop_id)

    def __str__(self):
        return "get_lines(stop_id={0})".format(self.__stop_id)

    @property
    def result(self):
        return self.__result

    def execute(self):
        self.__result = ruter.Line.from_stop_id(self.__stop_id)
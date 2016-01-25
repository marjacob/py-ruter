#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the representation of a line.
"""

from ruter import api


class Line(object):
    def __init__(self, json_source):
        self.__id = json_source["ID"]
        self.__color = json_source["LineColour"]
        self.__name = json_source["Name"]
        self.__transport = json_source["Transportation"]

    @property
    def color(self):
        """
        Gets the line identification color.
        """
        return self.__color

    @property
    def id(self):
        """
        Gets the ID of the line.
        """
        return self.__id

    @property
    def name(self):
        """
        Gets the name of the line.
        """
        return self.__name

    @property
    def transport(self):
        """
        Gets the transportation vehicle type.
        """
        return self.__transport

    @classmethod
    def from_stop_id(cls, stop_id):
        """
        Return the lines related to the stop.
        """
        return self.__from_json(api.get_lines_by_stop_id(stop_id))

    @staticmethod
    def __from_json(json_source):
        """
        Return a list of lines given a list of JSON entries.
        """
        return [Line(json_item) for json_item in json_source]

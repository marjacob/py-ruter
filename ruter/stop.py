#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the representation of a stop.
"""

import re

from requests.exceptions import HTTPError
from ruter import api
from ruter.departure import Departure
from ruter.line import Line
from ruter.location import Location


class Stop(object):
    def __init__(self, json_source):
        self.__district = json_source["District"]
        self.__id = json_source["ID"]
        self.__location = Location(json_source["X"], json_source["Y"])
        self.__name = json_source["Name"]
        self.__short_name = json_source["ShortName"]
        self.__zone = json_source["Zone"]

    @property
    def district(self):
        """
        Get the district in which the stop is located.
        """
        return self.__district

    @property
    def id(self):
        """
        Get the ID of the stop.
        """
        return self.__id

    @property
    def location(self):
        """
        Get the location coordinates of the stop.
        """
        return self.__location

    @property
    def name(self):
        """
        Get the name of the stop.
        """
        return self.__name

    @property
    def short_name(self):
        """
        Get the short version of the stop name.
        """
        return self.__short_name

    @property
    def zone(self):
        """
        Get the zone in which the stop is located.
        """
        return self.__zone

    def get_departures(self, time=None):
        """
        Return the departures from the stop.
        """
        return Departure.from_stop_id(stop_id=self.__id, time=time)

    def get_lines(self):
        """
        Return the lines connected to the stop.
        """
        return Line.from_stop_id(stop_id=self.__id)

    @classmethod
    def from_id(cls, stop_id):
        """
        Return information about a stop given its ID.
        """
        return Stop(ruter.api.get_stop(stop_id=stop_id))

    @classmethod
    def from_short_name(cls, short_name):
        """
        Return information about a stop given its unique short name.
        """
        json_source = api.get_stops_ruter()
        if len(json_source) > 0:
            reobj = re.compile("^{0}$".format(short_name), re.IGNORECASE)
            return next(Stop(item) for item in json_source
                        if reobj.match(item["ShortName"]))
        return None





#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains the representation of a departure.
"""

from ruter import api


class Departure(object):
    def __init__(self, json_source):
        json_extensions = json_source["Extensions"]
        json_journey = json_source["MonitoredVehicleJourney"]
        self.__colour = json_extensions["LineColour"]
        self.__destination = json_journey["DestinationName"]
        self.__line_id = json_journey["LineRef"]
        self.__name = json_journey["PublishedLineName"]
        self.__stop_id = json_source["MonitoringRef"]

    @property
    def colour(self):
        """
        Get the colour that identifies the line related to the departure.
        """
        return self.__colour

    @property
    def destination(self):
        """
        Get the destination name of the departing transport.
        """
        return self.__destination

    @property
    def line_id(self):
        """
        Get the line ID.
        """
        return self.__line_id

    @property
    def name(self):
        """
        Get the stop name.
        """
        return self.__name

    @property
    def stop_id(self):
        """
        Get the stop ID.
        """
        return self.__stop_id

    @classmethod
    def from_stop_id(cls, stop_id, time=None):
        """
        Return departures from a stop.
        """
        json_source = api.get_departures(stop_id, time)
        return cls.__list_from_json(json_source)

    @staticmethod
    def __list_from_json(json_source):
        """
        Return a list of departures given a list of JSON entries.
        """
        return [Departure(json_item) for json_item in json_source]

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains bindings for the RESTful ReisAPI offered by Ruter at
their endpoint https://reisapi.ruter.no
"""

import json
import requests

from datetime import datetime
from enum import Enum
from pytz import timezone


class TransportType(Enum):
    """
    Possible means of transportation.
    """
    airport_bus = 1
    airport_train = 4
    boat = 5
    bus = 2
    metro = 8
    train = 6
    tram = 7
    walking = 0


class ReisAPI(object):
    """
    The interface to ReisAPI.
    """
    def __init__(self):
        self.__base = "https://reisapi.ruter.no"

        # Minutes needed for interchange.
        # Max....: 99
        self.__change_margin = 2

        # Minutes punishment for an interchange.
        # Higher values prioritize journeys without interchange.
        # Max....: 199
        self.__change_punish = 8

        # Maximum number of proposals returned by the API.
        # Min....: 1
        # Max....: 40
        self.__max_proposals = 8

        # Maximum minutes a person should walk to a stop.
        # Max....: N/A (undocumented)
        self.__max_walking_minutes = 10

        # Walking speed in percent of default (which is 70 m/min).
        # Max....: 999
        self.__walking_factor = 100

    @property
    def change_margin(self):
        """
        Return the number of minutes needed for interchange.
        """
        return self.__change_margin

    @change_margin.setter
    def change_margin(self, value):
        """
        Set the number of minutes needed for interchange.
        """
        self.__change_margin = self.__enforce_range(1, 99, value)

    @property
    def change_punish(self):
        """
        Return the delay caused by an interchange in minutes.
        """
        return self.__change_punish

    @change_punish.setter
    def change_punish(self, value):
        """
        Set the delay caused by an interchange in minutes.
        """
        self.__change_punish = self.__enforce_range(1, 199, value)

    @property
    def max_proposals(self):
        """
        Return the maximum number of proposals.
        """
        return self.__max_proposals

    @max_proposals.setter
    def max_proposals(self, value):
        """
        Set the maximum number of proposals.
        """
        self.__max_proposals = self.__enforce_range(1, 40, value)

    # Favourites

    def get_favourites(self, favourites):
        """
        N/A
        """
        uri = "{0}/Favourites/GetFavourites".format(self.__base)
        params = {"favouritesRequest": favourites}
        return self.__process_response(requests.get(uri, params=params))

    # Heartbeat

    def ping(self):
        """
        Return a boolean value indicating whether the service is
        available.
        """
        uri = "{0}/Heartbeat/Index".format(self.__base)
        response = requests.get(uri)
        response.raise_for_status()
        return response.text == "\"Pong\""

    # Line

    def get_data_by_line_id(self, line_id):
        """
        Return data about a Line.
        """
        uri = "{base}/Line/GetDataByLineID/{line_id}" \
            .format(base=self.__base, line_id=line_id)
        return self.__process_response(requests.get(uri))

    def get_lines(self):
        """
        Return a List of all Lines available.
        """
        uri = "{0}/Line/GetLines".format(self.__base)
        return self.__process_response(requests.get(uri))

    def get_lines_by_stop_id(self, stop_id):
        """
        Return a List of all Lines that serve a Stop.
        """
        uri = "{base}/Line/GetLinesByStopID/{stop_id}" \
            .format(base=self.__base, stop_id=stop_id)
        return self.__process_response(requests.get(uri))

    def get_lines_ruter(self):
        """
        Return a list of lines that Ruter operates.
        """
        uri = "{0}/Line/GetLinesRuter".format(self.__base)
        return self.__process_response(requests.get(uri))

    def get_lines_ruter_extended(self):
        """
        Return a list of lines that Ruter operates, including stops
        for each line.
        """
        uri = "{0}/Line/GetLinesRuterExtended".format(self.__base)
        return self.__process_response(requests.get(uri))

    def get_stops_by_line_id(self, line_id):
        """
        Return a List of all Stops that are served by a Line.
        """
        uri = "{base}/Line/GetStopsByLineId/{line_id}" \
            .format(base=self.__base, line_id=line_id)
        return self.__process_response(requests.get(uri))

    # Meta

    def get_validities(self):
        """
        Return the date and time for the first and last valid search
        time.
        """
        uri = "{base}/Meta/GetValidities".format(base=self.__base)
        return self.__process_response(requests.get(uri))

    # Place

    def get_closest_stops(self, latitude, longtitude, max_distance=1400):
        """
        Return a list of stops and their real walking distance to the
        point indicated by the latitude and longtitude.
        """
        uri = "{base}/Place/GetClosestStops".format(base=self.__base)
        coordinates = "(X={0},Y={1})".format(latitude, longtitude)
        params = {"coordinates": coordinates,
                  "proposals": self.__max_proposals,
                  "maxdistance": max_distance}

        return self.__process_response(requests.get(uri, params=params))

    def get_places(self, search, county=None):
        """
        Return a list of places that have names similar to the search
        string. If a county is provided, search results are sorted
        according to geographical proximity.
        """
        uri = "{0}/Place/GetPlaces/{1}".format(self.__base, search)
        params = {}

        if county:
            params["counties"] = county

        return self.__process_response(requests.get(uri, params=params))

    def get_sale_points_by_area(self, longmin, longmax, latmin, latmax):
        """
        Returns a list of sale points within a box defined by the UTM33
        coordinates.
        """
        uri = "{0}/Place/GetSalePointsByArea".format(self.__base)
        params = {"longmin": longmin,
                  "longmax": longmax,
                  "latmin": latmin,
                  "latmax": latmax}

        return self.__process_response(requests.get(uri, params=params))

    def get_stop(self, stop_id):
        """
        Return all data about a stop.
        """
        uri = "{0}/Place/GetStop/{1}".format(self.__base, stop_id)
        return self.__process_response(requests.get(uri))

    def get_stops_by_area(self, xmin, ymin, xmax, ymax, stop_points=False):
        """
        Return a list of stops within a box defined by the UTM33
        coordinates.
        """
        uri = "{base}/Place/GetStopsByArea".format(base=self.__base)
        params = {"xmin": xmin,
                  "xmax": xmax,
                  "ymin": ymin,
                  "ymax": ymax,
                  "includeStopPoints": stop_points}

        return self.__process_response(requests.get(uri, params=params))

    def get_stops_ruter(self):
        """
        Return a list of stops within the Ruter zones.
        """
        uri = "{0}/Place/GetStopsRuter".format(self.__base)
        return self.__process_response(requests.get(uri))

    # StopVisit

    def get_departures(self, stop_id, transport=None, lines=None, time=None):
        """
        Return a list of departures from a stop.
        """
        uri = "{base}/StopVisit/GetDepartures/{stop_id}" \
            .format(base=self.__base, stop_id=stop_id)
        params = {}

        if time:
            params["datetime"] = time.strftime("%Y-%m-%d %H:%M:%S")

        if transport:
            params["transporttypes"] = transport

        if lines:
            params["linenames"] = lines

        return self.__process_response(requests.get(uri, params=params))

    # Street

    def get_street(self, street_id):
        """
        Return all houses of a street with their coordinates.
        """
        uri = "{base}/Street/GetStreet/{street_id}" \
            .format(base=self.__base, street_id=street_id)

        return self.__process_response(requests.get(uri))

    # Travel

    def get_travels(self, origin, destin, time=None, is_after=True):
        """
        Return possible journeys between two places.
        """
        uri = "{base}/Travel/GetTravels".format(base=self.__base)

        if not time:
            time = self.__get_oslo_time()

        params = {"fromPlace": origin,
                  "toPlace": destin,
                  "isafter": is_after,
                  "time": time.strftime("%d%m%Y%H%M%S"),
                  "changemargin": self.__change_margin,
                  "changepunish": self.__change_punish,
                  "walkingfactor": self.__walking_factor,
                  "proposals": self.__max_proposals,
                  "transporttypes": "",
                  "maxwalkingminutes": self.__max_walking_minutes,
                  "linenames": ""}

        return self.__process_response(requests.get(uri, params=params))

    # Trip

    def get_trip(self, trip_id, time=None):
        """
        Return a sequence of all stops served by a trip.
        """
        uri = "{base}/Trip/GetTrip/{trip_id}" \
            .format(base=self.__base, trip_id=trip_id)

        if not time:
            time = self.__get_oslo_time()

        params = {"time": time.strftime("%d%m%Y%H%M%S")}

        return self.__process_response(requests.get(uri, params=params))

    # Internals

    @staticmethod
    def __enforce_range(lower_bound, upper_bound, value):
        """
        Truncate a value to fit within a lower and upper bound.
        """
        if value < lower_bound:
            return lower_bound
        elif value > upper_bound:
            return upper_bound
        return value

    @staticmethod
    def __get_oslo_time(self):
        """
        Return the current time in Oslo, Norway.
        """
        return datetime.now(timezone("Europe/Oslo"))

    @staticmethod
    def __process_response(self, response):
        """
        Parse JSON and raise errors when appropriate.
        """
        response.raise_for_status()
        return json.loads(response.text)

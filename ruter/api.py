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


_endpoint = "https://reisapi.ruter.no"

# Minutes needed for interchange.
# Max....: 99
_change_margin = 2

# Minutes punishment for an interchange.
# Higher values prioritize journeys without interchange.
# Max....: 199
_change_punish = 8

# Maximum number of proposals returned by the API.
# Min....: 1
# Max....: 40
_max_proposals = 8

# Maximum minutes a person should walk to a stop.
# Max....: N/A (undocumented)
_max_walking_minutes = 10

# Walking speed in percent of default (which is 70 m/min).
# Max....: 999
_walking_factor = 100


def _enforce_range(lower_bound, upper_bound, value):
    """
    Truncate a value to fit within a lower and upper bound.
    """
    if value < lower_bound:
        return lower_bound
    elif value > upper_bound:
        return upper_bound
    return value


def _get_oslo_time():
    """
    Return the current time in Oslo, Norway.
    """
    return datetime.now(timezone("Europe/Oslo"))


def _process_response(response):
    """
    Parse JSON and raise errors when appropriate.
    """
    response.raise_for_status()
    return json.loads(response.text)


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


# Favourites

def get_favourites(favourites):
    """
    No description available from the official documentation.
    """
    uri = "{0}/Favourites/GetFavourites".format(_endpoint)
    params = {"favouritesRequest": favourites}
    return _process_response(requests.get(uri, params=params))

# Heartbeat

def ping():
    """
    Return a boolean value indicating whether the service is
    available.
    """
    uri = "{0}/Heartbeat/Index".format(_endpoint)
    response = requests.get(uri)
    response.raise_for_status()
    return response.text == "\"Pong\""

# Line

def get_data_by_line_id(line_id):
    """
    Return data about a Line.
    """
    uri = "{base}/Line/GetDataByLineID/{line_id}" \
        .format(base=_endpoint, line_id=line_id)
    return _process_response(requests.get(uri))

def get_lines():
    """
    Return a List of all Lines available.
    """
    uri = "{0}/Line/GetLines".format(_endpoint)
    return _process_response(requests.get(uri))

def get_lines_by_stop_id(stop_id):
    """
    Return a List of all Lines that serve a Stop.
    """
    uri = "{base}/Line/GetLinesByStopID/{stop_id}" \
        .format(base=_endpoint, stop_id=stop_id)
    return _process_response(requests.get(uri))

def get_lines_ruter():
    """
    Return a list of lines that Ruter operates.
    """
    uri = "{0}/Line/GetLinesRuter".format(_endpoint)
    return _process_response(requests.get(uri))

def get_lines_ruter_extended():
    """
    Return a list of lines that Ruter operates, including stops
    for each line.
    """
    uri = "{0}/Line/GetLinesRuterExtended".format(_endpoint)
    return _process_response(requests.get(uri))

def get_stops_by_line_id(line_id):
    """
    Return a List of all Stops that are served by a Line.
    """
    uri = "{base}/Line/GetStopsByLineId/{line_id}" \
        .format(base=_endpoint, line_id=line_id)
    return _process_response(requests.get(uri))

# Meta

def get_validities():
    """
    Return the date and time for the first and last valid search
    time.
    """
    uri = "{base}/Meta/GetValidities".format(base=_endpoint)
    return _process_response(requests.get(uri))

# Place

def get_closest_stops(latitude, longtitude, max_distance=1400):
    """
    Return a list of stops and their real walking distance to the
    point indicated by the latitude and longtitude.
    """
    uri = "{base}/Place/GetClosestStops".format(base=_endpoint)
    coordinates = "(X={0},Y={1})".format(latitude, longtitude)
    params = {"coordinates": coordinates,
              "proposals": _max_proposals,
              "maxdistance": max_distance}

    return _process_response(requests.get(uri, params=params))

def get_places(search, county=None):
    """
    Return a list of places that have names similar to the search
    string. If a county is provided, search results are sorted
    according to geographical proximity.
    """
    uri = "{0}/Place/GetPlaces/{1}".format(_endpoint, search)
    params = {}

    if county:
        params["counties"] = county

    return _process_response(requests.get(uri, params=params))

def get_sale_points_by_area(longmin, longmax, latmin, latmax):
    """
    Returns a list of sale points within a box defined by the UTM33
    coordinates.
    """
    uri = "{0}/Place/GetSalePointsByArea".format(_endpoint)
    params = {"longmin": longmin,
              "longmax": longmax,
              "latmin": latmin,
              "latmax": latmax}

    return _process_response(requests.get(uri, params=params))

def get_stop(stop_id):
    """
    Return all data about a stop.
    """
    uri = "{0}/Place/GetStop/{1}".format(_endpoint, stop_id)
    return _process_response(requests.get(uri))

def get_stops_by_area(xmin, ymin, xmax, ymax, stop_points=False):
    """
    Return a list of stops within a box defined by the UTM33
    coordinates.
    """
    uri = "{base}/Place/GetStopsByArea".format(base=_endpoint)
    params = {"xmin": xmin,
              "xmax": xmax,
              "ymin": ymin,
              "ymax": ymax,
              "includeStopPoints": stop_points}

    return _process_response(requests.get(uri, params=params))

def get_stops_ruter():
    """
    Return a list of stops within the Ruter zones.
    """
    uri = "{0}/Place/GetStopsRuter".format(_endpoint)
    return _process_response(requests.get(uri))

# StopVisit

def get_departures(stop_id, transport=None, lines=None, time=None):
    """
    Return a list of departures from a stop.
    """
    uri = "{base}/StopVisit/GetDepartures/{stop_id}" \
        .format(base=_endpoint, stop_id=stop_id)
    params = {}

    if time:
        params["datetime"] = time.strftime("%Y-%m-%d %H:%M:%S")

    if transport:
        params["transporttypes"] = transport

    if lines:
        params["linenames"] = lines

    return _process_response(requests.get(uri, params=params))

# Street

def get_street(street_id):
    """
    Return all houses of a street with their coordinates.
    """
    uri = "{base}/Street/GetStreet/{street_id}" \
        .format(base=_endpoint, street_id=street_id)

    return _process_response(requests.get(uri))

# Travel

def get_travels(origin, destin, time=None, is_after=True):
    """
    Return possible journeys between two places.
    """
    uri = "{base}/Travel/GetTravels".format(base=_endpoint)

    if not time:
        time = _get_oslo_time()

    params = {"fromPlace": origin,
              "toPlace": destin,
              "isafter": is_after,
              "time": time.strftime("%d%m%Y%H%M%S"),
              "changemargin": _change_margin,
              "changepunish": _change_punish,
              "walkingfactor": _walking_factor,
              "proposals": _max_proposals,
              "transporttypes": "",
              "maxwalkingminutes": _max_walking_minutes,
              "linenames": ""}

    return _process_response(requests.get(uri, params=params))

# Trip

def get_trip(trip_id, time=None):
    """
    Return a sequence of all stops served by a trip.
    """
    uri = "{base}/Trip/GetTrip/{trip_id}" \
        .format(base=_endpoint, trip_id=trip_id)

    if not time:
        time = _get_oslo_time()

    params = {"time": time.strftime("%d%m%Y%H%M%S")}

    return _process_response(requests.get(uri, params=params))

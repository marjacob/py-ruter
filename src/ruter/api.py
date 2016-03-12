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


RUTER_API_ENDPOINT = "https://reisapi.ruter.no"
RUTER_API_TIMEZONE = "Europe/Oslo"


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


def get_favourites(*args):
    """
    An application can store information about the user’s favourite departures
    from a Stop, filtered by Line and Destination. The FavouriteRequest is
    concatenated as such: Stopid1-lineid1-destinationtext1,stopid2-lineid2-
    destinationtext2 etc. Example: MonitoredStopVisits are returned, grouped
    by the three parametres.
    """
    if not len(args) > 0:
        return None
    favourites = []
    for arg in args:
        favourite = []
        # Origin (Stop ID)
        try:
            favourite.append(arg[0].id)
        except AttributeError:
            favourite.append(arg[0])
        # Line
        try:
            favourite.append(arg[1].id)
        except AttributeError:
            favourite.append(arg[1])
        # Destination
        try:
            favourite.append(arg[2].name)
        except AttributeError:
            favourite.append(arg[2])
        favourites.append("-".join(map(str, favourite)))
    uri = "{0}/Favourites/GetFavourites".format(RUTER_API_ENDPOINT)
    params = {"favouritesRequest": ",".join(favourites)}
    return __process_response(requests.get(uri, params=params))


def index():
    """
    Return a boolean value indicating whether the service is
    available.
    """
    uri = "{0}/Heartbeat/Index".format(RUTER_API_ENDPOINT)
    return __process_response(requests.get(uri))


def get_data_by_line_id(line_id):
    """
    Return data about a Line.
    """
    uri = "{0}/Line/GetDataByLineID/{1}".format(RUTER_API_ENDPOINT, line_id)
    return __process_response(requests.get(uri))


def get_lines():
    """
    Return a List of all Lines available.
    """
    uri = "{0}/Line/GetLines".format(RUTER_API_ENDPOINT)
    return __process_response(requests.get(uri))


def get_lines_by_stop_id(stop_id):
    """
    Return a List of all Lines that serve a Stop.
    """
    uri = "{0}/Line/GetLinesByStopID/{1}".format(RUTER_API_ENDPOINT, stop_id)
    return __process_response(requests.get(uri))


def get_lines_ruter():
    """
    Return a list of lines that Ruter operates.
    """
    uri = "{0}/Line/GetLinesRuter".format(RUTER_API_ENDPOINT)
    return __process_response(requests.get(uri))


def get_lines_ruter_extended():
    """
    Return a list of lines that Ruter operates, including stops
    for each line.
    """
    uri = "{0}/Line/GetLinesRuterExtended".format(RUTER_API_ENDPOINT)
    return __process_response(requests.get(uri))


def get_stops_by_line_id(line_id):
    """
    Return a List of all Stops that are served by a Line.
    """
    uri = "{0}/Line/GetStopsByLineId/{1}".format(RUTER_API_ENDPOINT, line_id)
    return __process_response(requests.get(uri))


def get_validities():
    """
    Return the date and time for the first and last valid search
    time.
    """
    uri = "{0}/Meta/GetValidities".format(RUTER_API_ENDPOINT)
    return __process_response(requests.get(uri))


def get_closest_stops(latitude, longtitude, **kwargs):
    """
    Return a list of stops and their real walking distance to the
    point indicated by the latitude and longtitude.
    """
    uri = "{0}/Place/GetClosestStops".format(RUTER_API_ENDPOINT)
    coordinates = "(X={0},Y={1})".format(latitude, longtitude)

    max_proposals = 25  # range(1, 40)
    if "max_proposals" in kwargs:
        max_proposals = min(max(1, kwargs["max_proposals"]), 40)

    max_distance = 1400
    if "max_distance" in kwargs:
        max_distance = max(0, kwargs["max_distance"])

    params = {"coordinates": coordinates,
              "proposals": max_proposals,
              "maxdistance": max_distance}

    return __process_response(requests.get(uri, params=params))


def get_places(search, county=None):
    """
    Return a list of places that have names similar to the search
    string. If a county is provided, search results are sorted
    according to geographical proximity.
    """
    uri = "{0}/Place/GetPlaces/{1}".format(RUTER_API_ENDPOINT, search)
    params = {}

    if county:
        params["counties"] = county

    return __process_response(requests.get(uri, params=params))


def get_sale_points_by_area(longmin, longmax, latmin, latmax):
    """
    Returns a list of sale points within a box defined by the UTM33
    coordinates.
    """
    uri = "{0}/Place/GetSalePointsByArea".format(RUTER_API_ENDPOINT)
    params = {"longmin": longmin,
              "longmax": longmax,
              "latmin": latmin,
              "latmax": latmax}

    return __process_response(requests.get(uri, params=params))


def get_stop(stop_id):
    """
    Return all data about a stop.
    """
    uri = "{0}/Place/GetStop/{1}".format(RUTER_API_ENDPOINT, stop_id)
    return __process_response(requests.get(uri))


def get_stops_by_area(xmin, ymin, xmax, ymax, stop_points=False):
    """
    Return a list of stops within a box defined by the UTM33
    coordinates.
    """
    uri = "{0}/Place/GetStopsByArea".format(RUTER_API_ENDPOINT)
    params = {"xmin": xmin,
              "xmax": xmax,
              "ymin": ymin,
              "ymax": ymax,
              "includeStopPoints": stop_points}

    return __process_response(requests.get(uri, params=params))


def get_stops_ruter():
    """
    Return a list of stops within the Ruter zones.
    """
    uri = "{0}/Place/GetStopsRuter".format(RUTER_API_ENDPOINT)
    return __process_response(requests.get(uri))


def get_departures(stop_id, transport=None, lines=None, time=None):
    """
    Return a list of departures from a stop.
    """
    uri = "{0}/StopVisit/GetDepartures/{1}".format(RUTER_API_ENDPOINT, stop_id)
    params = {}

    if time:
        params["datetime"] = time.strftime("%Y-%m-%d %H:%M:%S")

    if transport:
        params["transporttypes"] = transport

    if lines:
        params["linenames"] = lines

    return __process_response(requests.get(uri, params=params))


def get_street(street_id):
    """
    Return all houses of a street with their coordinates.
    """
    uri = "{0}/Street/GetStreet/{1}".format(RUTER_API_ENDPOINT, street_id)

    return __process_response(requests.get(uri))


def get_travels(origin, destin, time=None, is_after=True, **kwargs):
    """
    Return possible journeys between two places.
    """
    uri = "{0}/Travel/GetTravels".format(RUTER_API_ENDPOINT)

    if not hasattr(time, "strftime"):
        time = datetime.now(timezone(RUTER_API_TIMEZONE))

    params = {"fromPlace": origin,
              "toPlace": destin,
              "isafter": is_after,
              "time": time.strftime("%d%m%Y%H%M%S")}

    if "change_margin" in kwargs:
        params["changemargin"] = \
            min(max(1, kwargs["change_margin"]), 99)
    if "change_punish" in kwargs:
        params["changepunish"] = \
            min(max(1, kwargs["change_punish"]), 199)
    if "line_names" in kwargs:
        params["linenames"] = \
            ",".join(map(str, kwargs["line_names"]))
    if "max_proposals" in kwargs:
        params["proposals"] = \
            min(max(1, kwargs["max_proposals"]), 40)
    if "max_walking_minutes" in kwargs:
        params["maxwalkingminutes"] = \
            max(0, kwargs["max_walking_minutes"])
    if "transport_types" in kwargs:
        params["transporttypes"] = \
            ",".join(map(str, kwargs["transport_types"]))
    if "walking_factor" in kwargs:
        params["walkingfactor"] = \
            min(max(1, kwargs["walking_factor"]), 999)

    return __process_response(requests.get(uri, params=params))


def get_trip(trip_id, time=None):
    """
    Return a sequence of all stops served by a trip.
    """
    uri = "{0}/Trip/GetTrip/{1}".format(RUTER_API_ENDPOINT, trip_id)
    if not hasattr(time, "strftime"):
        time = datetime.now(timezone(RUTER_API_TIMEZONE))
    params = {"time": time.strftime("%d%m%Y%H%M%S")}
    return __process_response(requests.get(uri, params=params))


def __process_response(response):
    """
    Parse JSON and raise errors when appropriate.
    """
    response.raise_for_status()
    return json.loads(response.text)

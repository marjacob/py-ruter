#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ruter.api import ReisAPI


def main():
    api = ReisAPI()
    departures = api.get_departures(3010930)
    for departure in departures:
        journey = departure["MonitoredVehicleJourney"]
        print("{line}: {destination}".format(
            line=journey["PublishedLineName"],
            destination=journey["DestinationName"]))

if __name__ == "__main__":
    main()

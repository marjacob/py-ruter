#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from interfaces.observer import IObserver
from bus import ApiBus
from get_stop import GetStopCommand
from get_departures import GetDeparturesCommand
#import ruter


class Printer(IObserver):
    def __init__(self):
        self.__bus = ApiBus()
    def update(self, command):
        name = type(command).__name__
        print(name)

def main():
    bus = ApiBus()
    get_stop = GetStopCommand(3010930)
    get_departures = GetDeparturesCommand(3010930)
    p = Printer()
    
    bus.attach(p)
    bus.request(get_stop)
    bus.request(get_departures)
    bus.pump()

if __name__ == "__main__":
    main()





    # rosenholm = ruter.Stop.from_id(3010930)
    # national = ruter.Stop.from_short_name("roh")
    # departures = national.get_departures()
    # print("{name} in zone {zone} with ID {id}".format(
    #       name=national.name,
    #       zone=national.zone,
    #       id=national.id))
    # for departure in departures:
    #     print("{line}: {destination}".format(
    #         line=departure.line_id,
    #         destination=departure.destination))

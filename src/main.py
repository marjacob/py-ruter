#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import signal
import sys
import time

from interfaces.observer import IObserver
from bus import ApiBus

# Commands
from bus import AbortCommand
from get_stop_command import GetStopCommand
from get_departures_command import GetDeparturesCommand


class Main(IObserver):
    def __init__(self):
        self.__bus = ApiBus()
        self.__exit_code = 0
        signal.signal(signal.SIGINT, self.__signal_handler)
    def run(self):
        get_stop = GetStopCommand(3010930)
        get_departures = GetDeparturesCommand(3010930)

        self.__bus.attach(self)
        self.__bus.request(get_stop)
        self.__bus.request(get_departures)
        self.__bus.pump()

        return self.__exit_code
    def update(self, command):
        name = type(command).__name__
        print("\r{0}".format(name))
        if isinstance(command, AbortCommand):
            self.__exit_code = command.result
    def __signal_handler(self, signum, frame):
        self.__bus.request(AbortCommand(0))


if __name__ == "__main__":
    main = Main()
    sys.exit(main.run())





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

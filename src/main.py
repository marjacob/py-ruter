#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import signal
import sys
import time

import bus


class Main(bus.IObserver):
    """
    The main class encapsulating the shared variables required for the bus and
    signal handler to interface with each other.
    """
    def __init__(self):
        self.__bus = bus.CommandBus()
        self.__exit_code = 0
        signal.signal(signal.SIGINT, self.__signal_handler)

    def run(self):
        """
        Start the bus and begin processing commands.
        """
        get_stop = bus.GetStopCommand(3010930)
        get_departures = bus.GetDeparturesCommand(3010930)
        get_lines = bus.GetLinesCommand(3010930)

        self.__bus.attach(self)
        self.__bus.request(get_stop)
        self.__bus.request(get_departures)
        self.__bus.request(get_lines)

        # Process commands until an AbortCommand is queued.
        self.__bus.pump()

        return self.__exit_code

    def update(self, command):
        """
        Process completed commands.
        """
        name = type(command).__name__
        print("\r{0}".format(command))
        if isinstance(command, bus.AbortCommand):
            self.__exit_code = command.result

    def __signal_handler(self, signum, frame):
        """
        Post an AbortCommand to the pending queue of the bus.
        """
        self.__bus.stop()


if __name__ == "__main__":
    # Do not accept signals before the appropriate handler has been installed.
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main = Main()
    # Exit with the exit code specified by the AbortCommand.
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

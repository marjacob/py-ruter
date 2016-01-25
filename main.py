#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ruter


def main():
    rosenholm = ruter.Stop.from_id(3010930)
    national = ruter.Stop.from_short_name("roh")
    departures = national.get_departures()
    print("{name} in zone {zone} with ID {id}".format(
          name=national.name,
          zone=national.zone,
          id=national.id))
    for departure in departures:
        print("{line}: {destination}".format(
            line=departure.line_id,
            destination=departure.destination))

if __name__ == "__main__":
    main()

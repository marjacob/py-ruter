#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Location(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        """
        Get or set the X coordinate.
        """
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        """
        Get or set the Y coordinate.
        """
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

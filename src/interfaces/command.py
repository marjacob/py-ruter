#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

"""
This module contains the interface required to implement the Command pattern.
"""

import abc


class ICommand(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError()
    @abc.abstractproperty
    def result(self):
        raise NotImplementedError()

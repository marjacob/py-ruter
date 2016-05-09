#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

"""
This module contains the interface required to implement the Command pattern.
"""

import abc


class ISubject(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def attach(self, observer):
        raise NotImplementedError()
    @abc.abstractmethod
    def detach(self, observer):
        raise NotImplementedError()
    @abc.abstractmethod
    def notify(self):
        raise NotImplementedError()

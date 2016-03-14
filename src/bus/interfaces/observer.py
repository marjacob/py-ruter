#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

"""
This module contains the interface required to implement the Command pattern.
"""

import abc


class IObserver(object, metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def update(self, command):
		raise NotImplementedError()

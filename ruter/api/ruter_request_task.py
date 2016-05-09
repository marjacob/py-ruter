# -*- coding: utf-8 -*-


import json

import requests

from ruter.api.task import Task


class RuterRequestTask(Task):
    def __init__(self, path, **kwargs):
        self.__body = kwargs.get("body", None)
        self.__headers = kwargs.get("headers", None)
        self.__host = "http://reisapi.ruter.no"
        self.__method = kwargs.get("method", "GET")
        self.__params = kwargs.get("params", None)
        self.__path = path
        self.__session = requests.Session()
        self.__state = None

    def execute(self):
        request = requests.Request(
            data=self.__body,
            headers=self.__headers,
            method=self.__method, 
            params=self.__params,
            url="{0}{1}".format(self.__host, self.__path))
        
        prepared = request.prepare()
        response = self.__session.send(prepared)

        if not response.status_code == 200:
            return False
        else:
            self.__state = json.loads(response.text)

        return True
    
    @property
    def state(self):
        return self.__state

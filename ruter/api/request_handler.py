# -*- coding: utf-8 -*-


from  ruter.api.handler import Handler


class RequestHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self, task):
        pass



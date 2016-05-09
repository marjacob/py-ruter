# -*- coding: utf-8 -*-


from ruter.api.ruter_request_task import RuterRequestTask


class GetStopsRuterTask(RuterRequestTask):
    def __init__(self):
        super().__init__("/Place/GetStopsRuter")


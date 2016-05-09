# -*- coding: utf-8 -*-


from ruter.api.ruter_request_task import RuterRequestTask


class GetStopTask(RuterRequestTask):
    def __init__(self, stop_id):
        super().__init__("/Place/GetStop/{0}".format(stop_id))

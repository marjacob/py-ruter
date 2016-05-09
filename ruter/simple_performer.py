# -*- coding: utf-8 -*-


import abc
import queue
import threading

from ruter.performer import Performer
from ruter.stop_task import StopTask


class SimplePerformer(Performer):
    def __init__(self):
        self.__completed = queue.Queue()
        self.__customers = set()
        self.__pending = queue.Queue()
        self.__pool = set()

    def attach(self, customer):
        self.__customers.add(customer)

    def detach(self, customer):
        self.__customers.discard(customer)

    def start(self, threads=3):
        for i in range(0, threads):
            threading.Thread(
                args=(self.__pool, self.__pending, self.__completed),
                daemon=False,
                target=thread_main).start()
        while True:
            task = self.__completed.get(True)
            for customer in self.__customers:
                customer.update(task)
            if isinstance(task, StopTask):
                break

    def stop(self, exit_code=None):
        self.submit(StopTask(exit_code))

    def submit(self, task):
        self.__pending.put(task)


def thread_main(pool, pending, completed):
    this = threading.current_thread()
    pool.add(this)
    while True:
        task = pending.get(True)
        if isinstance(task, StopTask):
            pool.discard(this)
            if len(pool) > 0:
                completed.put(task)
            else:
                pending.put(task)
            break
        else:
            if task.execute():
                completed.put(task)
            else:
                pending.put(task)


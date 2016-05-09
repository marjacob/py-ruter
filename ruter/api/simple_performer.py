# -*- coding: utf-8 -*-


import abc
import queue
import threading

from ruter.api.customer import Customer
from ruter.api.performer import Performer
from ruter.api.stop_task import StopTask


class SimplePerformer(Performer):
    def __init__(self):
        self.__completed = queue.Queue()
        self.__customers = set()
        self.__pending = queue.Queue()
        self.__threads = 0

    def attach(self, customer):
        self.__customers.add(customer)

    def detach(self, customer):
        self.__customers.discard(customer)

    def start(self, threads=3):
        self.__threads = threads
        barrier = threading.Barrier(self.__threads)
        for i in range(0, self.__threads):
            threading.Thread(
                args=(barrier, self.__pending, self.__completed),
                daemon=False,
                target=thread_main).start()
        while True:
            task = self.__completed.get(True)
            for customer in self.__customers:
                customer.update(self, task)
            if isinstance(task, StopTask):
                return task.state

    def stop(self, exit_code=None):
        self.submit(StopTask(self.__threads, exit_code))

    def submit(self, task):
        self.__pending.put(task)


def thread_main(barrier, pending, completed):
    barrier.wait()
    while True:
        task = pending.get(True)
        stop = isinstance(task, StopTask)
        if task.execute():
            if stop:
                pending.put(task)
                break
            else:
                completed.put(task)
        else:
            if stop:
                completed.put(task)
                break
            else:
                pending.put(task)


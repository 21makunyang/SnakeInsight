import queue
import threading
import time

from loguru import logger

from snake_insight_threading.classes import Task
from snake_insight_threading.classes.HouseInfo import HouseInfo
from snake_insight_threading.common import STOP_SIGNAL


def _do_process(*args):
    newHouseInfo = []
    for h in args:
        if float(h.get('space')) < 1.0:
            continue
        newHouseInfo.append(h)
    return newHouseInfo


def do_process(task: Task) -> list[HouseInfo]:
    task.target = _do_process(task.target)
    return task.target


class Processor(threading.Thread):
    def __init__(self, in_queue: queue.Queue[Task], out_queue: queue.Queue[Task]):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

        self.__idle = True
        self.__last_work_time = 0

    def run(self):
        logger.info('Processor start running.')
        while True:
            task = self.in_queue.get()
            if task == STOP_SIGNAL:
                self.stop()
                break
            self.work()
            do_process(task)
            self.out_queue.put(task)
            self.free()

    def work(self):
        self.__idle = False

    def free(self):
        self.__idle = True
        self.__last_work_time = int(time.time())
        logger.debug(f'Processor is idle. Last work at {self.__last_work_time}')

    def idle_time(self) -> int:
        return int(time.time()) - self.__last_work_time if self.__idle else 0

    def stop(self):
        self.out_queue.put(STOP_SIGNAL)
        logger.info('Processor stopped.')

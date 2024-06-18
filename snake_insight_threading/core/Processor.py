import queue
import threading
import time

from loguru import logger

from snake_insight_threading.classes import Task
from snake_insight_threading.classes.HouseInfo import HouseInfo
from snake_insight_threading.common import STOP_SIGNAL


def _process_house_info(task: Task) -> list[HouseInfo]:
    assert isinstance(task.target, list)
    processed_house_info: list[HouseInfo] = []
    hi: HouseInfo
    for hi in task.target:
        if hi.space < 1.0:
            logger.debug(f'{hi} filtered. Reason: "space({hi.space}) < 1.0"')
            continue
        elif hi.floor == '':
            logger.debug(f'{hi} filtered. Reason: "floor is empty"')
            continue
        elif hi.advertisement == 'True':
            logger.debug(f'{hi} filtered. Reason: "advertisement({hi.advertisement}) == True"')
            continue
        processed_house_info.append(hi)
    return processed_house_info


def _do_process(task: Task) -> list[HouseInfo | Task]:
    if task.parser == 'Parser.HouseInfo':
        return _process_house_info(task=task)
    else:
        return task.target


def do_process(task: Task) -> list[HouseInfo | Task]:
    return _do_process(task)


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
            result = do_process(task)
            task.target = result
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

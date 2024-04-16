import queue
import random
import threading
import time

from loguru import logger
from requests import get, Response

from snake_insight_threading.classes import Task
from snake_insight_threading.common import STOP_SIGNAL
from snake_insight_threading.config.config import RANDOM_SLEEP, RANDOM_SLEEP_MAX, RANDOM_SLEEP_MIN


class TimedLock(object):
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self, timeout):
        self.lock.acquire()
        timer = threading.Timer(timeout, self.release)
        timer.daemon = True
        timer.start()

    def release(self):
        self.lock.release()

    def check(self):
        return self.lock.acquire()


locker = TimedLock()


def _do_get(url: str, *, random_sleep_ratio: float = 1.0) -> Response:
    response = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    if RANDOM_SLEEP:
        locker.acquire(random.randint(RANDOM_SLEEP_MIN, RANDOM_SLEEP_MAX) * random_sleep_ratio)
    try:
        response = get(url, headers=headers)
    except Exception as e:
        logger.info(f'response.get(url={url}) error: \n'
                    f'{e}')
    logger.info(f'Get response from {url}.')
    return response


def do_get(task: Task) -> Response:
    return _do_get(task.target, random_sleep_ratio=task.random_sleep_ratio)


class Spider(threading.Thread):
    def __init__(self, in_queue: queue.Queue[Task], out_queue: queue.Queue[Task]):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

        self.__idle = True
        self.__last_work_time = 0

    def add_task(self, task: Task):
        if isinstance(task.target, str):
            self.in_queue.put(task)
        else:
            logger.error(f'Spider.add_task(): task.target must be instance of str. Get {type(task.target)}.')

    def run(self):
        logger.info(f'Spider start running.')
        while True:
            task = self.in_queue.get()
            if task == STOP_SIGNAL:
                self.stop()
                break
            self.work()
            result = do_get(task)
            task.target = result
            self.out_queue.put(task)
            self.free()

    def work(self):
        self.__idle = False

    def free(self):
        self.__idle = True
        self.__last_work_time = int(time.time())
        logger.debug(f'Spider is idle. Last work at {self.__last_work_time}')

    def idle_time(self) -> int:
        return int(time.time()) - self.__last_work_time if self.__idle else 0

    def stop(self):
        self.out_queue.put(STOP_SIGNAL)
        logger.info(f'Spider stopped.')

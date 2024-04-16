import json
import queue
import threading
import time

from loguru import logger

from snake_insight_threading.classes import HouseInfo, TaskBitMap, PagedUrl
from snake_insight_threading.classes import Task
from snake_insight_threading.core import Spider, Parser, Processor
from snake_insight_threading.common import STOP_SIGNAL
from snake_insight_threading.util import RedisCommand


history = {}


class Controller(threading.Thread):
    redis = RedisCommand()

    def __init__(self, *, max_idle_time: int = None, idle_detection_time: int = None):
        super().__init__()

        self.task_queue = queue.Queue[Task]()
        self.result_queue = queue.Queue[Task]()
        self.spider_to_parser_queue = queue.Queue[Task]()
        self.parser_to_processor_queue = queue.Queue[Task]()

        self.spider = Spider(self.task_queue, self.spider_to_parser_queue)
        self.parser = Parser(self.spider_to_parser_queue, self.parser_to_processor_queue)
        self.processor = Processor(self.parser_to_processor_queue, self.result_queue)

        self.task_bit_map = TaskBitMap()

        if max_idle_time is None:
            self.max_idle_time = 5
        elif max_idle_time < 0:
            raise ValueError('"max_idle_time" must be a non-negative number.')
        else:
            self.max_idle_time = max_idle_time

        if idle_detection_time is None:
            self.idle_detection_time = 5
        elif idle_detection_time < 0:
            raise ValueError('"idle_detection_time" must be a non-negative number.')
        else:
            self.idle_detection_time = idle_detection_time

        self.prepare_stop = False

    def add_task(self, task: Task):
        self.task_bit_map.add_task(task=task)
        self.task_queue.put(task)
        logger.info(f'add_task: {task.__repr__()}')

    def is_all_idle(self):
        return (self.spider.idle_time() > self.max_idle_time
                and self.parser.idle_time() > self.max_idle_time
                and self.processor.idle_time() > self.max_idle_time)

    def run(self):
        self.spider.start()
        self.parser.start()
        self.processor.start()

        logger.info('Controller start running.')
        while True:
            try:
                task = self.result_queue.get(timeout=self.idle_detection_time)
                if task == STOP_SIGNAL and self.prepare_stop:
                    self.stop()
                    break

                if task.failed():
                    if len(task.target) == 0:
                        logger.warning(f'Task failed.\n'
                                       f'{task.task_info()}')
                    else:
                        task.retry()
                        self.task_queue.put(task)
                if isinstance(task.target, list):
                    self.task_bit_map.complete(task=task)
                    for sub_target in task.target:
                        if isinstance(sub_target, Task):
                            self.add_task(task=sub_target)
                        elif isinstance(sub_target, HouseInfo):
                            # TODO 结果收集
                            history[sub_target.id] = sub_target
                            self.redis.hset(sub_target)
                        else:
                            # TODO 类型不匹配
                            pass
                else:
                    # TODO 类型不匹配
                    pass

                if isinstance(task.url, PagedUrl):
                    task.target = task.url.next_page
                    if task.target is not None:
                        self.add_task(task=task)

            except queue.Empty:
                if self.is_all_idle():
                    logger.info('All threads are idle. Controller will be stopped soon.')
                    logger.info(f'{self.task_bit_map.get_map_info()}')
                    self.task_bit_map.save_history()
                    self.task_queue.put(STOP_SIGNAL)
                    self.prepare_stop = True

    def stop(self):
        with open(f'log/history_{int(time.time())}.json', 'w+') as jf:
            json.dump(history, jf)
        logger.info('Controller stopped.')

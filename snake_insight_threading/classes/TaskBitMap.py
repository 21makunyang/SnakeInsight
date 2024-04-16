import json
import time

from snake_insight_threading.classes import Task


class TaskBitMap(object):
    INCOMPLETE = '□'
    COMPLETE = '■'

    def __init__(self):
        self.__bit_map: dict[str, list[str]] = {}
        self.__task_history = []

        self.__max_prefix_len = 0

    def add_task(self, task: Task) -> Task:
        self.__max_prefix_len = self.__max_prefix_len if self.__max_prefix_len > len(task.group) else len(task.group)
        self.__bit_map[task.group] = self.__bit_map.get(task.group, [])
        task.id = len(self.__bit_map[task.group])
        self.__bit_map[task.group].append(self.INCOMPLETE)
        self.__task_history.append(task.archive())
        return task

    def complete(self, task: Task):
        self.__bit_map[task.group][task.id] = self.COMPLETE

    def get_map_info(self):
        map_info = (f'Get task bit map info.\n'
                    f'-------------Task Bit Map-------------\n')
        for group, bit_map in self.__bit_map.items():
            map_info += f'{group:{self.__max_prefix_len}} | {" ".join(bit_map)}\n'
        map_info += f'--------------------------------------\n'
        return map_info

    def save_history(self):
        with open(f'log/taskHistory_{int(time.time())}.json', 'w+') as his:
            json.dump(self.__task_history, his)

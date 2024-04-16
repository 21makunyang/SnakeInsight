from loguru import logger
from requests import Response

from snake_insight_threading.classes import PagedUrl


class TaskInfo(object):
    def __init__(self):
        self.city = ''
        self.region = ''
        self.area = ''
        self.page = 1


class Task(object):
    RANDOM_SLEEP_RATIO = [1.0, 1.2, 1.5]

    def __init__(self, *,
                 id_: int = None,
                 group: str,
                 parser_index: int = None,
                 parser_sequence: str | list[str],
                 url: str | PagedUrl,
                 target: str | list,
                 max_retry: int = None):
        # 任务id
        self.id = -1 if id_ is None else id_
        self.group = group
        # 解析器
        self.parser_index = 0 if parser_index is None else parser_index
        if isinstance(parser_sequence, str):
            self.parser_sequence = [parser_sequence]
        else:
            self.parser_sequence = parser_sequence
        self.url: str | PagedUrl = url
        # 目标，可以是网址，中间结果，最终输出
        self.target: str | Response | list = target
        self.__retry = 0
        self.__max__retry = 3 if max_retry is None else max_retry
        # Spider获取信息时的随机间隔倍率
        self.random_sleep_ratio = self.RANDOM_SLEEP_RATIO[self.__retry]

    @property
    def parser(self) -> str:
        return self.parser_sequence[self.parser_index]

    @property
    def next_parser(self):
        if self.parser_index + 1 < len(self.parser_sequence):
            return self.parser_sequence[self.parser_index + 1]
        else:
            return None

    def next(self):
        self.parser_index += 1

    def failed(self):
        return self.__retry >= self.__max__retry

    def retry(self):
        if not self.failed() and len(self.target) == 0:
            self.__retry += 1
            self.random_sleep_ratio = self.RANDOM_SLEEP_RATIO[self.__retry]

    def subtask(self, *, subgroup, url, target):
        return Task(group=f'{self.group}-{subgroup}',
                    parser_index=self.parser_index + 1,
                    parser_sequence=self.parser_sequence,
                    url=url,
                    target=target)

    def batch(self):
        pass

    def task_info(self):
        return (f'-------------Task Info-------------\n'
                f'            id: {self.id}\n'
                f'parserSequence: {self.parser_sequence} (now at parser[{self.parser_index}])\n'
                f'        target: {self.target}\n'
                f'-----------------------------------\n')

    def __repr__(self):
        return f'Task(id = {self.id}, group = {self.group}, target = "{str(self.target)[:100]}")'

    def interrupt(self, reason=None):
        logger.warning(f'Task has been interrupted. (Reason: {reason})\n'
                       f'{self.task_info()}')

    def archive(self):
        return {"id": self.id,
                "group": self.group,
                "parser_sequence": self.parser_sequence,
                "target": self.target if isinstance(self.target, str) else type(self.target)}

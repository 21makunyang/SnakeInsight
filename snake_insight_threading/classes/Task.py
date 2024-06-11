from loguru import logger
from requests import Response

from snake_insight_threading.classes import PagedUrl


class Task(object):
    RANDOM_SLEEP_RATIO = [1.0, 1.2, 1.5]

    def __init__(self, *,
                 id_: int = -1,
                 group: str,
                 parser_index: int = 0,
                 parser_sequence: str | list[str],
                 url: str | PagedUrl,
                 target: str | list,
                 max_retry: int = 3,
                 strict_interrupt: bool = False):
        # 任务id
        self.id = id_
        self.group = group
        # 解析器
        self.parser_index = parser_index
        # 将parser_sequence转为列表
        if isinstance(parser_sequence, str):
            self.parser_sequence = [parser_sequence]
        else:
            self.parser_sequence = parser_sequence
        self.url: str | PagedUrl = url
        # 目标，可以是网址，中间结果，最终输出
        self.target: str | Response | list = target
        self.__retry: int = 0
        self.__max__retry: int = max_retry
        # Spider获取信息时的随机间隔倍率
        self.random_sleep_ratio: float = self.RANDOM_SLEEP_RATIO[self.__retry]
        self.__interrupted: bool = False
        self.__strict_interrupt: bool = strict_interrupt
        self.__completed: bool = False

    @property
    def parser(self) -> str:
        return self.parser_sequence[self.parser_index]

    @property
    def next_parser(self):
        if self.parser_index + 1 < len(self.parser_sequence):
            return self.parser_sequence[self.parser_index + 1]
        else:
            return None

    @property
    def interrupted(self):
        return self.__interrupted

    @property
    def strict_interrupt(self):
        return self.__strict_interrupt

    # @strict_interrupt.fset
    # def strict_interrupt(self, _strict):
    #     self.__strict_interrupt = _strict

    @property
    def completed(self):
        return self.__completed

    def next(self):
        self.parser_index += 1

    def failed(self):
        return self.__retry >= self.__max__retry

    def retry(self):
        if not self.failed() and len(self.target) == 0:
            self.__interrupted = False
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
        self.__interrupted = True
        logger.warning(f'Task has been interrupted. (Reason: {reason})\n'
                       f'{self.task_info()}')

    def archive(self):
        return {"id": self.id,
                "group": self.group,
                "parser_sequence": self.parser_sequence,
                "target": self.target if isinstance(self.target, str) else type(self.target)}

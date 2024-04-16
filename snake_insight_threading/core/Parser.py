import json
import queue
import re
import threading
import time

from bs4 import BeautifulSoup
from loguru import logger
from requests import Response

from snake_insight_threading.classes import Task, PagedUrl
from snake_insight_threading.classes.HouseInfo import HouseInfo
from snake_insight_threading.common import STOP_SIGNAL


def _parse_house_info(task: Task) -> list[HouseInfo]:
    house_info_list = []
    try:
        bs = BeautifulSoup(task.target.text, 'html.parser')

        house_info_code_block_list = bs.find_all(class_='zu-itemmod clearfix')
        for house_info_code_block in house_info_code_block_list:
            info_code_block = house_info_code_block.find(class_=['zu-info'])
            advertisement = house_info_code_block.find(class_=['jx-sign']) is not None
            price_code_block = house_info_code_block.find(class_=['zu-side'])

            id_code = house_info_code_block.a['href']
            title_code = house_info_code_block.h3.a
            detail_code_block = info_code_block.find_all(class_=['details-item'])

            house_info = detail_code_block[0].find_all(class_=['strongbox'])
            address_info = detail_code_block[1]
            tag_info = detail_code_block[2]

            house_info_list.append(HouseInfo(
                id_=re.search(r'fangyuan/(\d+)[?]', id_code).group(1),
                title=title_code.text.strip(),
                bedroom=int(house_info[0].text),
                living_room=int(house_info[1].text),
                space=float(house_info[2].text),
                floor=detail_code_block[0].contents[-1].strip(),
                community=address_info.a['href'],
                tags=list([tag.text for tag in tag_info.find_all(class_=['cls-common'])]),
                advertisement=advertisement,
                price=int(price_code_block.find(class_=['price']).text),
                unit=price_code_block.find(class_=['unit']).text,
                raw=house_info_code_block.text,
                city=task.group.split('-')[0],
                area=address_info.contents[2].strip(),
                region=address_info.contents[4].strip()
            ))
    except Exception as e:
        task.interrupt(e)
        logger.warning(e.__traceback__)
    return house_info_list


def _parse_region_url(task: Task) -> list[Task]:
    task_list = []
    try:
        bs = BeautifulSoup(task.target.text, 'html.parser')

        region_url_code_block = bs.find(class_='sub-items sub-level1')
        region_url_code_list = region_url_code_block.find_all(name='a')
        for code in region_url_code_list:
            if code.text != '全部' and code.text != '':
                if task.next_parser == 'Parser.HouseInfo':
                    url = PagedUrl(code['href'])
                else:
                    url = code['href']
                task_list.append(task.subtask(subgroup=code.text, url=url, target=code['href']))
    except Exception as e:
        task.interrupt(e)
    return task_list


def _parse_area_url(task: Task) -> list[Task]:
    if not isinstance(task.target, Response):
        logger.warning(f'task.target must be instance of Response. Get {type(task.target)}.')
        return []
    task_list = []
    try:
        bs = BeautifulSoup(task.target.text, 'html.parser')

        region_url_code_block = bs.find(class_='sub-items sub-level2')
        region_url_code_list = region_url_code_block.find_all(name='a')
        for code in region_url_code_list:
            if code.text != '全部' and code.text != '':
                if task.next_parser == 'Parser.HouseInfo':
                    url = PagedUrl(code['href'])
                else:
                    url = code['href']
                task_list.append(task.subtask(subgroup=code.text, url=url, target=code['href']))
    except Exception as e:
        task.interrupt(e)
    return task_list


def _do_parse(task: Task) -> list[HouseInfo | Task]:
    if task.parser == 'Parser.HouseInfo':
        parsed_list = _parse_house_info(task=task)
        return parsed_list
    elif task.parser == 'Parser.RegionUrlTask':
        return _parse_region_url(task=task)
    elif task.parser == 'Parser.AreaUrlTask':
        return _parse_area_url(task=task)
    else:
        message = (f'task.parser must be "Parser.HouseInfo", "Parser.RegionUrlTask" or "Parser.AreaUrlTask". '
                   f'Get "{task.parser}".')
        task.interrupt(message)


def do_parse(task: Task) -> list[HouseInfo | Task]:
    return _do_parse(task)


class Parser(threading.Thread):
    def __init__(self, in_queue: queue.Queue[Task], out_queue: queue.Queue[Task]):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

        self.__idle = True
        self.__last_work_time = 0

    def run(self):
        logger.info('Parser start running.')
        while True:
            task = self.in_queue.get()
            if task == STOP_SIGNAL:
                self.stop()
                break
            self.work()
            result = do_parse(task)
            task.target = result
            self.out_queue.put(task)
            self.free()

    def work(self):
        self.__idle = False

    def free(self):
        self.__idle = True
        self.__last_work_time = int(time.time())
        logger.debug(f'Parser is idle. Last work at {self.__last_work_time}')

    def idle_time(self) -> int:
        return int(time.time()) - self.__last_work_time if self.__idle else 0

    def stop(self):
        self.out_queue.put(STOP_SIGNAL)
        logger.info('Parser stopped.')

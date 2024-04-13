import random
import threading

from fake_useragent import UserAgent
from requests import get, Response

from snake_insight.classes import PagedUrl
from snake_insight.config.config import RANDOM_SLEEP, RANDOM_SLEEP_MAX, RANDOM_SLEEP_MIN
from snake_insight.util import getLogger
from snake_insight.util.decorator import entry_debug


class TimedLock(object):
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self, timeout):
        self.lock.acquire()
        timer = threading.Timer(timeout, self.release)
        timer.start()

    def release(self):
        self.lock.release()

    def check(self):
        return self.lock.acquire()


UA = UserAgent()
locker = TimedLock()

logger = getLogger('SI.core.spider')


@entry_debug(logger)
def _do_get(url: str) -> Response:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    if RANDOM_SLEEP:
        locker.acquire(random.randint(RANDOM_SLEEP_MIN, RANDOM_SLEEP_MAX))
    response = get(url, headers=headers)
    logger.info(f'Get response from {url}.')
    return response


@entry_debug(logger)
def get_info(paged_url: PagedUrl) -> list[Response]:
    response_list = []

    for url in paged_url:
        response_list.append(_do_get(url))

    return response_list

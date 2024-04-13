from inspect import getframeinfo, currentframe

from snake_insight.config.config import ENTRY_DEBUG
from snake_insight.util import to_module_path


def entry_debug(logger):
    def wrapper(func):
        def inner(*args, **kwargs):
            if ENTRY_DEBUG:
                file_path, line, _, _, _ = getframeinfo(currentframe().f_back)
                message = f'{to_module_path(abs_path=file_path[:-3])}:{line} | call {func.__name__}'
                logger.debug(message)
            return func(*args, **kwargs)

        return inner

    return wrapper

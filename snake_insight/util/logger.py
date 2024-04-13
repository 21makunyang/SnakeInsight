import time

from snake_insight.common import console
from snake_insight.config.config import LOGGING_LEVEL

loguru_inited = False


def getLogger(name: str = ''):
    logging_file = f'log/{time.strftime("%Y%m%d%H%M%S")}.log'
    try:
        from loguru import logger

        global loguru_inited
        if not loguru_inited:
            logger.info('Use loguru as log module.')
            logger.level(LOGGING_LEVEL)
            logger.add(logging_file, level=LOGGING_LEVEL)
            loguru_inited = True

        return logger
    except ImportError:
        import logging
        logging.basicConfig(level=LOGGING_LEVEL,
                            format='%(asctime)s [%(levelname)s] | %(name)s - %(message)s',
                            filename=logging_file)
        logger = logging.getLogger(name=name)
        logger.addHandler(console)
        logger.setLevel(LOGGING_LEVEL)

        logger.info('Use logging as log module.')

        return logger

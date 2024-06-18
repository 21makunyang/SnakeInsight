import sys
import time

from loguru import logger

from snake_insight_threading.config.config import LOGGING_LEVEL


logger.remove(0)

logger.add(
    sys.stdout,
    level=LOGGING_LEVEL
)

# loguru.logger init
logging_file = f'log/{time.strftime("%Y%m%d%H%M%S")}.log'

logger.info(f'Use loguru as log module. Log file at "{logging_file}"')
logger.level(LOGGING_LEVEL)
logger.add(logging_file, level=LOGGING_LEVEL)

import logging

from snake_insight.config.config import LOGGING_LEVEL

# 使用logging模块进行日志输出时，需要配置参数使其能输出日志到控制台
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s - %(message)s')

console.setLevel(LOGGING_LEVEL)
console.setFormatter(formatter)

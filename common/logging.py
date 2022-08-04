# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/6/30 20:15
# @File    : logging.py


import sys
import time
from loguru import logger
import config
# 最先实现的log日志方法，但在pytest中无法实现控制台的实时日志输入


class Logger:

    def __init__(self, level: str = "DEBUG", colorlog: bool = True):
        self.logger = logger
        self._colorlog = colorlog
        self._console_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</> {file} <level>| {level} | {message}</level>"
        self._level = level

    def set_level(self, colorlog: bool = True, format: str = None, level: str = "DEBUG"):
        if format is None:
            format = self._console_format
        logger.remove()
        logger.add(sys.stderr, level=level, colorize=colorlog, format=format)

    def trace(self, msg: str):
        if config.print_log is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | TRACE | {str(msg)}")
        return self.logger.trace(msg)

    def debug(self, msg: str):
        if config.print_log is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | DEBUG | {str(msg)}")
        return self.logger.debug(msg)

    def info(self, msg: str):
        if config.print_log is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | INFO | {str(msg)}")
        return self.logger.info(msg)

    def success(self, msg: str):
        if config.print_log is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | SUCCESS | {str(msg)}")
        return self.logger.success(msg)

    def warning(self, msg: str):
        if config.print_log is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | WARNING | {str(msg)}")
        return self.logger.warning(msg)

    def error(self, msg: str):
        if config.print_log is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | ERROR | {str(msg)}")
        return self.logger.error(msg)

    def critical(self, msg: str):
        if config.print_log is True:
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} | CRITICAL | {str(msg)}")
        return self.logger.critical(msg)

    def printf(self, msg: str):
        return self.logger.success(msg)


# log level: TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR
log = Logger(level="TRACE")

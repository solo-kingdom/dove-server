# coding: utf-8
import os
from configparser import ConfigParser
import logging
import logging.handlers

import sys


class MyLogger(object):

    def __init__(self, log_file_name=None, log_file_path=None):
        # 读取配置文件
        self.config = ConfigParser()
        log_config_file_path = os.path.join(os.path.dirname(__file__), 'log-config.ini')
        if not os.path.exists(log_config_file_path):
            print("配置文件 log-config.ini 不存在.")
        self.config.read(log_config_file_path)

        # 获取日志保存路径
        self.log_file_path = self.config.get('config', 'path')
        # 日志文件名称
        self.log_file_name = self.config.get('config', 'name')
        # 获取日志文件大小
        self.log_file_size = self.config.getint('config', 'size') * 1024 * 1024
        # 获取日志文件数量
        self.log_file_num = self.config.getint('config', 'num')

        if log_file_path is not None:
            # 如果自定义了日志路径
            self.log_file_path = log_file_path

        if log_file_name is not None:
            # 如果自定义了日志文件名
            self.log_file_name = log_file_name
        self.log_file_full_path = os.path.join(os.path.dirname(__file__), self.log_file_path, self.log_file_name)

        # 初始化logger
        self.logger = logging.getLogger()
        # 日志格式
        fmt = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s',
                                '%Y-%m-%d %H:%M:%S')

        # 日志输出到文件，这里用到了上面获取的日志名称，大小，保存个数

        handle1 = logging.handlers.RotatingFileHandler(self.log_file_full_path, maxBytes=self.log_file_size,
                                                       backupCount=self.log_file_num)
        handle1.setFormatter(fmt)
        handle1.setLevel(logging.WARNING)

        # 同时输出到屏幕，便于实施观察
        handle2 = logging.StreamHandler(stream=sys.stdout)
        handle2.setFormatter(fmt)

        self.logger.addHandler(handle1)
        self.logger.addHandler(handle2)
        handle2.setLevel(logging.WARNING)

    def debug(self, msg):
        self.logger.debug(msg)
        return

    def info(self, msg):
        self.logger.info(msg)
        return

    def warning(self, msg):
        self.logger.warning(msg)
        return

    def error(self, msg):
        self.logger.error(msg)
        return

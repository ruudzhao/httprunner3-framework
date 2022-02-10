import sys
import logging
import os
from icecream import ic

#  ic.disable()


class HttpRunner3Logger:
    def __init__(self):
        logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

        logging_file_path = "{}{}{}".format(os.path.abspath(os.path.curdir), os.path.sep, "httprunner3.log")
        # ic(logging_file_path)

        self.logger = logging.getLogger("httprunner3")
        handler = logging.FileHandler(logging_file_path, encoding='UTF-8')
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging_format)
        self.logger.addHandler(handler)

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging_format)
        self.logger.addHandler(handler)

        self.logger.setLevel(logging.DEBUG)

        ic("logger init finished.")


__app_logger = HttpRunner3Logger()
logger = __app_logger.logger

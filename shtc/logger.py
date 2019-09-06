import sys
import logging
from shtc.patterns import Singleton


class Logger(object, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(name='Logger')
        self.log.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '[%(asctime)s] - [%(levelname)s]: %(module)s(%(lineno)s) - %(message)s'
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.WARNING)
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)

        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

    def __call__(self):
        return self.log

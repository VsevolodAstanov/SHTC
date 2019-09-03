import sys
import logging


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=Singleton):

    def __init__(self):
        self._logger = logging.getLogger(name='Logger')
        self._logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '[%(asctime)s] - [%(levelname)s]: %(module)s(%(lineno)s) - %(message)s'
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.WARNING)
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

        file_handler = logging.FileHandler('tagcounter.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def __call__(self):
        return self._logger

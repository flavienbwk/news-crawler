import logging
import logging.handlers
import os

from slugify import slugify


PROJECT_NAME = slugify(os.environ.get("PROJECT_NAME", "project"), separator="_")
CRAWLER_SOURCE = slugify(os.environ.get("CRAWLER_SOURCE"), separator="_")

FILE_PATH = os.path.realpath(__file__)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = f"{DIR_PATH}/../../logs"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self) -> bool:
        log_path = f"{LOGS_DIR}/{PROJECT_NAME}_{CRAWLER_SOURCE}.log"
        handler = logging.handlers.WatchedFileHandler(log_path)
        log_file_format = (
            f"[%(levelname)s - %(asctime)s - %(name)s - {CRAWLER_SOURCE}] %(message)s"
        )
        log_console_format = (
            f"[%(levelname)s - %(asctime)s - {CRAWLER_SOURCE}] %(message)s"
        )
        handler.setFormatter(logging.Formatter(log_file_format))
        main_logger = logging.getLogger("NewsCrawler")
        main_logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
        main_logger.addHandler(handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
        console_handler.setFormatter(logging.Formatter(log_console_format))
        main_logger.addHandler(console_handler)
        self.root = main_logger

    def debug(self, message):
        self.root.debug(message)

    def info(self, message):
        self.root.info(message)

    def warning(self, message):
        self.root.warning(message)

    def error(self, message):
        self.root.error(message)

    def critical(self, message):
        self.root.critical(message)

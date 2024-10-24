"""Singleton module implementing logger and history manager."""
import logging
from factory import DataFacade

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.strategy = None
        self.logger = logging.getLogger(__name__)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def log(self, message, level):
        if self.strategy:
            self.strategy.log(message, level)
        else:
            self.logger.log(getattr(logging, level), message)

    def get_logger(self):
        return self.logger

class HistoryManager(metaclass=SingletonMeta):
    def __init__(self):
        self.facade = DataFacade()

    def add_record(self, operation, num1, num2, result):
        self.facade.add_record(operation, num1, num2, result)

    def save_to_csv(self, filename):
        return self.facade.save_to_csv(filename)

    def load_from_csv(self, filename):
        return self.facade.load_from_csv(filename)

    def view_data(self):
        return self.facade.view_data()

    def clear_data(self):
        return self.facade.clear_data()

# Create an instance of Logger
logger_instance = Logger()

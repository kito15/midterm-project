import pandas as pd

class HistoryStrategy:
    def save(self, data, filename):
        raise NotImplementedError

    def load(self, filename):
        raise NotImplementedError

class CSVHistoryStrategy(HistoryStrategy):
    def save(self, data, filename):
        data.to_csv(filename, index=False)

    def load(self, filename):
        return pd.read_csv(filename)

class LoggerStrategy:
    def log(self, message, level):
        raise NotImplementedError

class FileLoggerStrategy(LoggerStrategy):
    def __init__(self, filename):
        self.filename = filename

    def log(self, message, level):
        with open(self.filename, 'a') as file:
            file.write(f"{level}: {message}\n")

class ConsoleLoggerStrategy(LoggerStrategy):
    def log(self, message, level):
        print(f"{level}: {message}")

class Logger:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def log(self, message, level):
        self.strategy.log(message, level)

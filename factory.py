from .facade import DataFacade

class HistoryManagerFactory:
    @staticmethod
    def create_history_manager():
        return DataFacade()

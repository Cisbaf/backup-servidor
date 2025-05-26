import docker
import os
import time
from datetime import timedelta
from abc import ABC, abstractmethod
from utils.logger import get_logger
from utils.path import find_folder_path



logger = get_logger("Backup Cisbaf")
handle_logger = {
    'error': lambda message: logger.critical(message),
    'warning': lambda message: logger.warning(message),
    'info': lambda message: logger.info(message),
    'critical': lambda message: logger.critical(message),
}

class BackupRepository(ABC):

    def __init__(self):
        self.name = self.__class__.__name__
        self.docker = docker.from_env()
        self.loggs = []
        self.path_backup = ""
        self._config_path_()

    def _config_path_(self):
        _path = os.path.join(find_folder_path("setup/backups"), self.name.lower())
        if not os.path.exists(_path):
            os.mkdir(_path)
        self.path_backup = find_folder_path(f"setup/backups/{self.name.lower()}")

    def register_log(self, type: str, message: str):
        if type in handle_logger:
            handler = handle_logger[type]
            self.loggs.append(lambda: handler(f"{self.name} > {message}"))

    def _execute_logs_(self):
        for log in self.loggs:
            log()
    
    @abstractmethod
    def set_up(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def start(self):
        try:
            start_time = time.time()
            self.set_up()
            self.run()
        except Exception as e:
            self.register_log("critical", f"Exception > {str(e)} ")
        finally:
            end_time = time.time()
            elapsed = end_time - start_time
            formatted_time = str(timedelta(seconds=int(elapsed)))
            self.register_log("info", f"Backup Finalizado! Tempo total: {formatted_time}")
            self._execute_logs_()

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from utils.path import find_folder_path

def get_logger(name: str = "default_logger") -> logging.Logger:
    log_dir = find_folder_path("setup/logs")
    os.makedirs(log_dir, exist_ok=True)

    # Nome base do arquivo (sempre sobrescrito com data no handler)
    base_filename = os.path.join(log_dir, "log")

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )

        # Cria handler com rotação diária, mantém últimos 7 dias
        handler = TimedRotatingFileHandler(
            base_filename,
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8',
            utc=False
        )
        handler.setFormatter(formatter)
        handler.suffix = "%d-%m-%Y.log"  # Nome do arquivo com data D-M-Y

        logger.addHandler(handler)

    return logger

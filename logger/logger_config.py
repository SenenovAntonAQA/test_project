import os
import logging


class LoggerConfig:
    LOGS_DIR_NAME = "logs"  # директория куда сохраняем
    LOGGER_NAME = "Logger"  # имя логера
    LOGS_FILE_NAME = LOGS_DIR_NAME + os.sep + "test.log"  # имя файла логирования

    LOGS_LEVEL = logging.INFO  # уровень логера (ниже игнорирует)

    MAX_BYTES = 100000  # максимальный размер файла с логами
    BACKUP_COUNT = 10  # кол-во файлов с логами

    FORMAT = "[%(asctime)s - %(levelname)s] - %(message)s"
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

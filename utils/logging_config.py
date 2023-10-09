import logging
import os


def configure_logger(logger_name: str, log_file: str) -> logging.Logger:
    """
    Configure and return a logger object.

    Args:
        logger_name (str): The name of the logger.
        log_file (str): The path to the log file.

    Returns:
        logging.Logger: A configured Logger object.
    """
    log_format = "%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s | line:%(lineno)d | %(message)s"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(handler)

    return logger


def create_log_folder(log_folder: str) -> None:
    """
    Create the log folder if it doesn't exist.

    Args:
        log_folder (str): The path to the log folder.
    """
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)


log_folder: str = "logs/"
create_log_folder(log_folder=log_folder)

error_logger = configure_logger("error_logger", f"{log_folder}error_logger.log")
info_logger = configure_logger("info_logger", f"{log_folder}info_logger.log")
warning_logger = configure_logger("warning_logger", f"{log_folder}warning_logger.log")
exception_logger = configure_logger(
    "exception_logger", f"{log_folder}exception_logger.log"
)

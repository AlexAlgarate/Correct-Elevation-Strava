import logging
import os


class BaseLogger(logging.Logger):
    """
    Base logger class

    """

    def __init__(self, name: str, log_file_path: str, log_level: int) -> None:
        super().__init__(name, level=log_level)
        self.log_file_path = log_file_path
        self._create_log_file_directory()
        self._create_file_handler()

    def _create_log_file_directory(self) -> None:
        """
        Creates the directory for the log file if it doesn't exist

        """
        if not os.path.exists(os.path.dirname(self.log_file_path)):
            os.mkdir(os.path.dirname(self.log_file_path))

    def _create_file_handler(self) -> None:
        """
        Creates a new file handler for the logger
        """
        handler = logging.FileHandler(self.log_file_path)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)


class ErrorLogger(BaseLogger):
    """
    Custom logger class for logging errors to a file.

    """

    def __init__(
        self,
        name: str = "error_logger",
        log_file_path: str = "logger\\logger_errors.log"
    ) -> None:
        super().__init__(name, log_file_path, logging.ERROR)


class InfoLogger(BaseLogger):
    """
    Custom logger class for logging info to a file.

    """

    def __init__(
        self, name: str = "info_logger", log_file_path: str = "logger\\logger_info.log"
    ) -> None:
        super().__init__(name, log_file_path, logging.INFO)


class WarningLogger(BaseLogger):
    """
    Custom logger class for logging info to a file.

    """

    def __init__(
        self,
        name: str = "warning_logger",
        log_file_path: str = "logger\\warning_logger.log"
    ) -> None:
        super().__init__(name, log_file_path, logging.WARNING)

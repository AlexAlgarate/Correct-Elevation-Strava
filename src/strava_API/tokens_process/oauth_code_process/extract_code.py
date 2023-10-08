import logging
import re
from typing import Optional

from selenium.webdriver.chrome.webdriver import WebDriver

from logger.logger import ErrorLogger


class ExtractCode:
    driver: WebDriver
    """
    Class responsible for extracting the OAuth code from Strava's authorization URL.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def _extract_code(self) -> str:
        """
        Extracts the OAuth code from Strava's authorization URL.

        Returns:
            - The OAuth code extracted from the URL, or None if not found.
        """
        authorizated_url: str = self.driver.current_url
        # reg_expression: Pattern[str] = compile("&code=([\a-z]+)&")
        # code_match: Match[str] | None = reg_expression.search(authorizated_url)
        code_match: Optional[re.Match[str]] = re.search(
            r"&code=([\w]+)&", authorizated_url
        )

        if not code_match:
            logging.error("Could not retrieve OAuth code from URL")
            # ErrorLogger(self).error(msg="Could not retrieve OAuth code from URL")
            return None

        return code_match.group(1)

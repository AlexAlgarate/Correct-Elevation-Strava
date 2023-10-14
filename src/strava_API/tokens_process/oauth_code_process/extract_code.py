import re

from selenium.webdriver.chrome.webdriver import WebDriver

from utils import err_log


class ExtractCode:
    driver: WebDriver
    """
    Class responsible for extracting the OAuth code from Strava's authorization URL.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def extract_code(self) -> str:
        """
        Extracts the OAuth code from Strava's authorization URL.

        Returns:
            - The OAuth code extracted from the URL, or None if not found.
        """
        authorized_url: str = self.driver.current_url
        code_match: re.Match | None = re.search(r"&code=([\w]+)&", authorized_url)

        if not code_match:
            err_log.error("Could not retrieve OAuth code from URL")
            return None

        return code_match.group(1)

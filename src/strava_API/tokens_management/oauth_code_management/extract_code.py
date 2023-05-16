import re

from selenium.webdriver.chrome.webdriver import WebDriver

from logger.logger import ErrorLogger


class ExtractCode:
    driver: WebDriver
    """
    Class responsible for extracting the OAuth code from Strava's authorization URL.
    Methods:
        - extract_code(driver: WebDriver) -> str: extracts the OAuth code from the URL.
    Attributes:
        - driver: WebDriver object used to navigate the web page.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def _extract_code(self) -> str:
        """
        Extracts the OAuth code from Strava's authorization URL.
        Returns:
            - The OAuth code extracted from the URL.
        """
        authorizated_url = self.driver.current_url
        reg_expression = re.compile("&code=([\a-z]+)&")
        code_match = reg_expression.search(authorizated_url)

        if not code_match:
            ErrorLogger.error("Could not retrieve OAuth code from URL")

        return code_match.group(1)

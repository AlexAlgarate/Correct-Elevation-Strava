from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from config import seconds, url_to_get_OAuth_code
from logger.logger import ErrorLogger
from src.strava_api.tokens_process.oauth_code_process.extract_code import ExtractCode
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
import time

error_logger = ErrorLogger()


class GetOauthCode:
    """
    Class responsible for getting the OAuth code
    required to obtain the access token.

    Methods:
        - code_to_get_access_token() -> str: gets the OAuth code required
        to obtain the access token.
    """

    def get_oauth_code(self) -> str:
        """
        Gets the OAuth code required to obtain the access token.

        Returns:
            - The OAuth code required to obtain the access token.
        """
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        ) as driver:
            driver.implicitly_wait(seconds)
            try:
                strava = LoginStrava(driver)
                get_code = ExtractCode(driver)

                strava.login()

                driver.get(url_to_get_OAuth_code)
                strava._click_button(By.CSS_SELECTOR, "button#authorize")
                time.sleep(2)
                return get_code._extract_code()
            except Exception as e:
                error_logger.error(f"Error: {e}")

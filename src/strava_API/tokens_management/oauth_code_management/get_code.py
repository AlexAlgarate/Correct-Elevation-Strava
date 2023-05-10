from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import EMAIL, PASSWORD, seconds, url_to_get_OAuth_code
from src.logger.logger import ErrorLogger
from src.correct_elevation.credentials import Credentials
from src.strava_api.tokens_management.oauth_code_management.click_authorize import (
    ClickAuthorize,
)
from src.strava_api.tokens_management.oauth_code_management.extract_code import (
    ExtractCode,
)
from src.strava_api.tokens_management.oauth_code_management.login_into_strava import (
    Strava,
)

error_logger = ErrorLogger()


class GetCode:
    """
    Class responsible for getting the OAuth code required to obtain the access token.
    Methods:
        - code_to_get_access_token() -> str: gets the OAuth code required
        to obtain the access token.
    """

    def code_to_get_access_token(self) -> str:
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
                credentials = Credentials(EMAIL, PASSWORD)
                strava = Strava(driver)
                authorize_button = ClickAuthorize(driver)
                get_code = ExtractCode(driver)
                strava.login(credentials)
                driver.get(url_to_get_OAuth_code)
                authorize_button._click_authorize(driver)
                return get_code._extract_code()
            except Exception as e:
                error_logger.error(f"Error: {e}")

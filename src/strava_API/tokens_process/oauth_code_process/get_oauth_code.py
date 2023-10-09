import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.strava_api.tokens_process.oauth_code_process.extract_code import ExtractCode
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils import exc_log
from utils.config import seconds, url_to_get_OAuth_code


class GetOauthCode:
    """
    Class responsible for getting the OAuth code
    required to obtain the access token.

    Methods:
        - get_oauth_code() -> str: gets the OAuth code required
        to obtain the access token.
    """

    def get_oauth_code(self) -> str:
        """
        Gets the OAuth code required to obtain the access token.

        Returns:
            - The OAuth code required to obtain the access token.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)

        with webdriver.Chrome(service=Service(), options=options) as driver:
            driver.implicitly_wait(seconds)
            try:
                strava = LoginStrava(driver)
                get_code = ExtractCode(driver)

                strava.login()

                driver.get(url_to_get_OAuth_code)
                authorize_button = strava._find_element(
                    function=EC.element_to_be_clickable,
                    locator=By.CSS_SELECTOR,
                    selector="button#authorize",
                )
                strava._click_button(authorize_button)
                time.sleep(2)
                return get_code._extract_code()
            except Exception as e:
                exc_log.exception(e)

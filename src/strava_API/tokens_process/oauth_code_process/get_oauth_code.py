from time import sleep
from typing import Any

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.strava_api.tokens_process.oauth_code_process.extract_code import ExtractCode
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils import exc_log
from utils.config import seconds, url_OAuth


class OauthCodeGetter:
    """
    A class responsible for obtaining the OAuth code needed to obtain an access token

    Methods:
        - get_oauth_code() -> str: Retrieves the required OAuth code for acquiring an access token.
    """

    def get_oauth_code(self) -> str:
        """
        Retrieves the OAuth code neccessary to obtain an access token.

        Returns:
            str: The required  OAuth codefor obtaining an access token.
        """
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)

        with Chrome(service=Service(), options=options) as driver:
            driver.implicitly_wait(seconds)
            try:
                strava = LoginStrava(driver)
                get_code = ExtractCode(driver)

                strava.login()

                driver.get(url_OAuth)
                authorize_button: Any | None = strava.find_element(
                    function=EC.element_to_be_clickable,
                    locator=By.CSS_SELECTOR,
                    selector="button#authorize",
                )
                strava.click_button(authorize_button)
                sleep(2)
                return get_code.extract_code()

            except Exception as e:
                exc_log.exception(e)

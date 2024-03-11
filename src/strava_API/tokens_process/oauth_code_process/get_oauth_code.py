from __future__ import annotations

from time import sleep

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement

from src.strava_api.tokens_process.oauth_code_process.extract_code import ExtractCode
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils import exc_log
from utils.config import OAuth_url, seconds
from utils.locators import oauth_elements
from utils.web_element_handler import WebElementHandler


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
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_experimental_option("detach", True)

        with Chrome(service=Service(), options=options) as driver:
            driver.implicitly_wait(time_to_wait=seconds)
            try:
                strava = LoginStrava(driver=driver)
                get_code = ExtractCode(driver=driver)
                web_elements = WebElementHandler(driver=driver)

                strava.login()

                web_elements.open_url(url=OAuth_url)
                authorize_button: WebElement = web_elements.find_element(
                    *oauth_elements["authorize_button"]
                )

                web_elements.click_button(element=authorize_button)
                sleep(1)
                return get_code.extract_code()

            except Exception as e:
                exc_log.exception(e)

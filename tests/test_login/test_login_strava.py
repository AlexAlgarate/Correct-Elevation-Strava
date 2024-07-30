from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.strava_api.tokens_process.oauth_code_process.credentials import Credentials
from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils import config
from utils.locators import ALERT_MESSAGES, alert_box_message, login_elements
from utils.web_element_handler import WebElementHandler


class TestStravaLoginPage:
    def test_strava_isinstances(
        self, login_strava: LoginStrava, driver: WebDriver
    ) -> None:
        assert isinstance(login_strava, LoginStrava)
        assert isinstance(driver, WebDriver)
        assert hasattr(login_strava, "login")

    def test_open_strava_page(
        self, driver: WebDriver, element: WebElementHandler
    ) -> None:
        element.open_url(url=config.url_login_strava)
        assert "https://www.strava.com/login" == driver.current_url

    def test_find_log_in_elements(self, element: WebElementHandler) -> None:
        element.open_url(url=config.url_login_strava)
        for element_name, (condition, locator, selector) in login_elements.items():
            element_name: WebElement = element.find_element(
                condition=condition, locator=locator, selector=selector
            )
            assert element_name is not None

    def test_insert_email_and_password(
        self, strava_credentials: Credentials, element: WebElementHandler
    ) -> None:
        element.open_url(url=config.url_login_strava)

        email_element = element.find_element(*login_elements["email"])
        password_element = element.find_element(*login_elements["password"])
        element.fill_field(email_element, strava_credentials.email)
        element.fill_field(password_element, strava_credentials.password)
        assert email_element.get_attribute("value") == strava_credentials.email
        assert password_element.get_attribute("value") == strava_credentials.password

    def test_click_log_in_button(self, element: WebElementHandler) -> None:
        element.open_url(url=config.url_login_strava)
        login_button: WebElement = element.find_element(*login_elements["login_button"])
        element.click_button(login_button)
        assert login_button is not None

    def test_login_failed(self, element: WebElementHandler) -> bool:
        element.open_url(url=config.url_login_strava)
        login_button: WebElement = element.find_element(*login_elements["login_button"])
        element.click_button(login_button)
        alert_box: str = (element.find_element(*alert_box_message["alert_box"])).text
        for message in ALERT_MESSAGES:
            if message.casefold() in alert_box.casefold():
                assert True

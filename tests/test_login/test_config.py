import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils.web_element_handler import WebElementHandler


@pytest.fixture
def driver() -> WebDriver:
    options = ChromeOptions()
    # options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    driver = Chrome(service=Service(), options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login_strava(driver: WebDriver) -> LoginStrava:
    login_strava = LoginStrava(driver)
    login_strava.login()
    return login_strava


@pytest.fixture
def element(driver: WebDriver) -> WebElementHandler:
    return WebElementHandler(driver)

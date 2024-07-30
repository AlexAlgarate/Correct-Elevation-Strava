import pytest
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from src.strava_api.tokens_process.oauth_code_process.login_strava import LoginStrava
from utils.web_element_handler import WebElementHandler


@pytest.fixture
def driver():
    options = ChromeOptions()
    # options.add_argument("--start-maximized")
    arguments = [
        "--headless",
        "--disable-gpu",
        "--disable-extensions",
    ]
    for args in arguments:
        options.add_argument(args)
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-extensions")
    options.page_load_strategy = "eager"
    driver = Chrome(service=Service(), options=options)
    yield driver
    driver.quit()


@pytest.fixture
def login_strava(driver: WebDriver) -> LoginStrava:
    login_instance = LoginStrava(driver)
    login_instance.login()
    return login_instance


@pytest.fixture
def element(driver: WebDriver) -> WebElementHandler:
    return WebElementHandler(driver)

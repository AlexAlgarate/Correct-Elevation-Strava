from typing import List, Tuple, Union

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from utils.config import strava_login_url
from src.correct_elevation.credentials import Credentials
from src.strava_api.tokens_process.oauth_code_process.extract_code import (
    ExtractCode as EC,
)
from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import (
    GetOauthCode as GOC,
)

WEB_ELEMENTS_TO_FIND: List[
    Tuple[
        Union[
            expected_conditions.visibility_of_element_located,
            expected_conditions.element_to_be_clickable,
        ],
        By,
        str,
    ]
] = [
    (expected_conditions.visibility_of_element_located, By.ID, "email"),
    (expected_conditions.visibility_of_element_located, By.ID, "password"),
    (
        expected_conditions.element_to_be_clickable,
        By.CSS_SELECTOR,
        "button.btn.btn-primary",
    ),
]


@pytest.fixture
def driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(), options=options)
    yield driver
    driver.quit()


class TestExtractCode:
    def test_extract_code_if_exists(self, driver):
        driver.get("https://example.com/&code=abcdef&other_params=123")
        extracted_code = EC(driver)._extract_code()
        assert extracted_code == "abcdef"

    def test_extract_code_when_not_found(self, driver):
        driver.get("https://example.com/&other_params=123")
        extracted_code = EC(driver)._extract_code()
        assert extracted_code is None

    def test_extract_code_error_handling(self, driver, caplog):
        driver.get("https://example.com/?other_params=123")
        extract_code = EC(driver)
        extracted_code = extract_code._extract_code()
        assert extracted_code is None
        assert "Could not retrieve OAuth code from URL" in caplog.text

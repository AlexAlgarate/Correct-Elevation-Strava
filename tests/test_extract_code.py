from typing import List, Tuple, Union

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.strava_api.tokens_process.oauth_code_process.extract_code import (
    ExtractCode,
)


WEB_ELEMENTS_TO_FIND: List[
    Tuple[
        Union[
            EC.visibility_of_element_located,
            EC.element_to_be_clickable,
        ],
        By,
        str,
    ]
] = [
    (EC.visibility_of_element_located, By.ID, "email"),
    (EC.visibility_of_element_located, By.ID, "password"),
    (
        EC.element_to_be_clickable,
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
    def test_extract_code_if_exists(self, driver) -> None:
        driver.get("https://example.com/&code=holacaracola&other_params=123")
        extracted_code = ExtractCode(driver).extract_code()
        assert extracted_code == "holacaracola"

    def test_extract_code_when_not_found(self, driver) -> None:
        driver.get("https://example.com/&other_params=123")
        extracted_code = ExtractCode(driver).extract_code()
        assert extracted_code is None

    def test_extract_code_error_handling(self, driver, caplog) -> None:
        driver.get("https://example.com/?other_params=123")
        extract_code = ExtractCode(driver)
        extracted_code = extract_code.extract_code()
        assert "Could not retrieve OAuth code from URL" in caplog.text
        assert extracted_code is None

    def test_extract_code_with_multiple_matches(self, driver) -> None:
        driver.get("https://example.com/&code=abc&other_params=123&code=def")
        extracted_code = ExtractCode(driver).extract_code()
        assert extracted_code == "abc"

    def test_extract_code_with_special_characters(self, driver) -> None:
        driver.get("https://example.com/&code=gh%20ij&other_params=123")
        extracted_code = ExtractCode(driver).extract_code()
        assert extracted_code is None

    def test_extract_code_with_malformed_url(self, driver) -> None:
        driver.get("https://example.com/code=malformed")
        extracted_code = ExtractCode(driver).extract_code()
        assert extracted_code is None

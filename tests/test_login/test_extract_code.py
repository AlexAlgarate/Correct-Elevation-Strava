import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from src.strava_api.tokens_process.oauth_code_process.extract_code import ExtractCode


@pytest.fixture
def driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(service=Service(), options=options)
    yield driver
    driver.quit()


class TestExtractCode:
    def test_extract_code_if_exists(self, driver) -> None:
        driver.get("https://example.com/&code=BikeTimeTri&other_params=123")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code == "BikeTimeTri"

    def test_extract_code_error_handling(self, driver, caplog) -> None:
        driver.get("https://example.com/?other_params=123")
        extract_code = ExtractCode(driver)
        extracted_code: str = extract_code.extract_code()
        assert "Could not retrieve OAuth code from URL" in caplog.text
        assert extracted_code is None

    def test_extract_first_code_with_multiple_matches(self, driver) -> None:
        driver.get("https://example.com/&code=abc&other_params=123&code=def")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code == "abc"

    def test_none_with_special_characters(self, driver) -> None:
        driver.get("https://example.com/&code=gh%20ij&other_params=123")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code is None

    def test_extract_code_with_malformed_url(self, driver) -> None:
        driver.get("https://example.com/code=malformed")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code is None

from selenium.webdriver import Chrome

from src.strava_API.tokens_process.oauth_code_process.extract_code import ExtractCode


class TestExtractCode:
    def test_extract_code_if_exists(self, driver: Chrome) -> bool:
        driver.get("https://example.com/&code=BikeTimeTri&other_params=123")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code == "BikeTimeTri"

    def test_extract_code_error_handling(self, driver: Chrome, caplog) -> bool:
        driver.get("https://example.com/?other_params=123")
        extract_code = ExtractCode(driver)
        extracted_code: str = extract_code.extract_code()
        assert "Could not retrieve OAuth code from URL" in caplog.text
        assert extracted_code is None

    def test_extract_first_code_with_multiple_matches(self, driver: Chrome) -> bool:
        driver.get("https://example.com/&code=abc&other_params=123&code=def")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code == "abc"

    def test_none_with_special_characters(self, driver: Chrome) -> bool:
        driver.get("https://example.com/&code=gh%20ij&other_params=123")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code is None

    def test_extract_code_with_malformed_url(self, driver: Chrome) -> bool:
        driver.get("https://example.com/code=malformed")
        extracted_code: str = ExtractCode(driver).extract_code()
        assert extracted_code is None

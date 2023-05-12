from __future__ import annotations

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import seconds
from logger.logger import ErrorLogger, InfoLogger
from src.correct_elevation.credentials import Credentials

info_logger = InfoLogger()
error_logger = ErrorLogger()


class LoginStravaOauthCode:
    driver: WebDriver = None
    web_driver_wait: WebDriverWait = None

    def __init__(self, driver: WebDriver):
        self.driver = driver
        driver.get("https://www.strava.com/login")
        self.web_driver_wait = WebDriverWait(driver, seconds)

    def _fill_fields(self, locator: By, selector: str) -> None:
        field = self.web_driver_wait.until(
            EC.visibility_of_element_located((locator, selector))
        )
        return field

    def _click_button(self, locator: By, selector: str) -> None:
        button = self.web_driver_wait.until(
            EC.element_to_be_clickable((locator, selector))
        )
        return button

    def login(self, credentials: Credentials) -> LoginStravaOauthCode:
        try:
            email_field = self._fill_fields(By.ID, "email")
            password_field = self._fill_fields(By.ID, "password")
            login_button = self._click_button(By.CSS_SELECTOR, "button.btn.btn-primary")

            email_field.send_keys(credentials.email)
            password_field.send_keys(credentials.password)
            login_button.click()
        except (NoSuchElementException, TimeoutError) as e:
            error_logger.error(f"Error: {e}")
    # def login(self, credentials: Credentials) -> LoginStravaOauthCode:
    #     try:
    #         email_field = self.web_driver_wait.until(
    #             EC.visibility_of_element_located((By.ID, "email"))
    #         )
    #         password_field = self.web_driver_wait.until(
    #             EC.visibility_of_element_located((By.ID, "password"))
    #         )
    #         login_button = self.web_driver_wait.until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
    #         )

    #         email_field.send_keys(credentials.email)
    #         password_field.send_keys(credentials.password)
    #         login_button.click()
    #     except (NoSuchElementException, TimeoutError, Exception) as e:
    #         error_logger.error(f"Error: {e}")
    #     finally:
    #         return self

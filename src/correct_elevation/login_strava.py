from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import EMAIL, PASSWORD, seconds
from src.utils.logger import ErrorLogger, InfoLogger

error_logger = ErrorLogger()
info_logger = InfoLogger()


class LoginStrava:
    @staticmethod
    def fill_email(driver) -> None:
        """
        Fill in the email field on the Strava login page

        Args:
            - The Selenium webdriver instance to use

        Rerturns:
            None
        """
        email_field = WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "email"
                )
            )
        )
        email_field.send_keys(EMAIL)
        
        return self

    @staticmethod
    def fill_password(driver) -> None:
        """
        Fill in the password field on the Strava login page

        Args:
            - The Selenium webdriver instance to use

        Rerturns:
            None

        """
        password_field = WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys(PASSWORD)

    @staticmethod
    def click_login_button(driver) -> None:
        """
        Clicks on the Strava login page

        Args:
            - The Selenium webdriver instance to use

        Rerturns:
            None

        """
        login_button = WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        login_button.click()

    def login(self, driver) -> None:
        """
        Login into Strava using the given Selenium webdriver.

        """
        try:
            driver.get("https://www.strava.com/login")
            self.fill_email(driver)
            self.fill_password(driver)
            self.click_login_button(driver)
            info_logger.info("You are in Stava!")

        except (NoSuchElementException, TimeoutError, Exception) as e:
            error_logger.error(f"Error: {e}")

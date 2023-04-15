from typing import List
from config import EMAIL, PASSWORD, seconds
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from logger.logger import ErrorLogger, InfoLogger
import time

error_logger = ErrorLogger()
info_logger = InfoLogger()


class GetACtivityURL:
    @staticmethod
    def get_activity_url(activity_id: int) -> str:
        """
        Returns the URL of the Strava activity given an activity ID.

        Returns:
            A string of the URL of the activity

        """
        return f"https://www.strava.com/activities/{activity_id}"


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
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(EMAIL)

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


class CorrectElevation:

    """
    A class to correct the elevation data of a Strava
    activity using a Selenium webdriver.

    """

    def __init__(self, activity_ids: List[int]) -> None:
        self.activity_ids = activity_ids
        self.get_url = GetACtivityURL()
        self.login = LoginStrava()

    @staticmethod
    def _is_activity_indoor_cycling(driver) -> bool:
        """
        Returns whether or not the current activity is an
        indoor cycling activity.

        """
        try:
            indoor_cycling = "spinning"
            header = WebDriverWait(driver, seconds).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h2.text-title3.text-book.marginless")
                )
            )
            activity_type = (
                WebDriverWait(header, seconds)
                .until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
                .text
            )

            if indoor_cycling.casefold() in activity_type.casefold():
                return True

        except NoSuchElementException:
            return False

    @staticmethod
    def _click_options_button(driver) -> None:
        """
        _click_options_button _summary_

        Args:
            driver (_type_): _description_
        """
        options_button = WebDriverWait(driver, seconds).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.app-icon.icon-nav-more"))
        )
        options_button.click()
        time.sleep(2)
        # options_button = WebDriverWait(driver, seconds).until(
        #     EC.element_to_be_clickable(
        #         (
        #             By.CLASS_NAME,
        #             "app-icon.icon-nav-more"
        #         )
        #     )
        # )
        # options_button.click()

    @staticmethod
    def _click_correct_elevation_option(driver) -> None:
        correct_elevation_option = WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-react-class='CorrectElevation']")
            )
        )
        correct_elevation_option.click()
        time.sleep(2)

    @staticmethod
    def _click_correct_elevation(driver) -> None:
        seconds = 15
        # Click on the button to correct the activity
        correct_activity_button = WebDriverWait(driver, seconds).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button"
                    # "button.Button--btn--E4CP9.Button--primary--cUgAV"
                )
            )
        )
        correct_activity_button.click()

    def run(self) -> None:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)
        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        ) as driver:
            self.login.login(driver)
            for i, activity in enumerate(self.activity_ids):
                print(f"#_#_\nProcessing activity {activity}\n")
                activity_url = self.get_url.get_activity_url(activity)
                driver.get(activity_url)
                print(f"#_#_\nActivity: {activity}\n")
                if self._is_activity_indoor_cycling(driver):
                    print(f"#_#_\nDetected indoor cycling activity {activity}")
                    if i < len(self.activity_ids) - 1:
                        continue
                else:
                    self._click_options_button(driver)
                    self._click_correct_elevation_option(driver)
                    self._click_correct_elevation(driver)
                    driver.implicitly_wait(20)
                    # self.correct_activity(driver)
                    print(f"\nElevation has corrected for activity:{activity}")
        driver.quit()

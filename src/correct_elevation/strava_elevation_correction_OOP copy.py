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

from src.utils.logger import ErrorLogger
import time


class GetACtivityURL:
    @staticmethod
    def get_activity_url(activity_id: int) -> str:
        """
        Returns the URL of the Strava activity given an activity ID.

        """
        return f"https://www.strava.com/activities/{activity_id}"


class CorrectElevation:

    """
    A class to correct the elevation data of a Strava
    activity using a Selenium webdriver.

    """

    def __init__(self, activity_ids: List[int]):
        self.activity_ids = activity_ids
        self.logger = ErrorLogger()
        self.get_url = GetACtivityURL()

    def get_activity_url(self, activity_id: int) -> str:
        """
        Returns the URL of the Strava activity given an activity ID.

        """
        return f"https://www.strava.com/activities/{activity_id}"

    def login(self, driver) -> None:
        """
        Logs into Strava using the given Selenium webdriver.

        """
        driver.get("https://www.strava.com/login")

        # Fill in the email and password fields
        email_field = WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(EMAIL)

        password_field = WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys(PASSWORD)
        # Click on the login button
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

    def is_activity_indoor_cycling(self, driver) -> bool:
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
            # header = WebDriverWait(driver, seconds).until(
            #     EC.presence_of_element_located((
            #         By.CLASS_NAME, "text-title3.text-book.marginless"
            #     ))
            # )

            activity_type = (
                WebDriverWait(header, seconds)
                .until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
                .text
            )
            if indoor_cycling.casefold() in activity_type.casefold():
                return True

        except NoSuchElementException:
            return False

    def correct_activity(self, driver) -> None:
        options_button = WebDriverWait(driver, seconds).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "slide-menu.drop-down-menu.enabled.align-top")
            )
        )
        options_button.click()

        correct_elevation_option = WebDriverWait(driver, seconds).until(
            EC.element_to_be_clickable(
                (By.XPATH, '(//*[@id="react-list-item"]/div/a)[2]')
            )
        )

        correct_elevation_option.click()

        # Click on the button to correct the activity
        correct_activity_button = WebDriverWait(driver, seconds).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button",
                )
            )
        )
        correct_activity_button.click()

        driver.implicitly_wait(15)

    def run(self) -> None:
        # Set the options that you need
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        # Start the driver
        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        ) as driver:
            # Run the log in process
            self.login(driver)
            for i, activity in enumerate(self.activity_ids):
                print(f"Processing activity {activity}")

                activity_url = self.get_url.get_activity_url(activity)
                driver.get(activity_url)
                print(f"Activity: {activity}")
                time.sleep(5)
                if self.is_activity_indoor_cycling(driver):
                    print(f"Detected indoor cycling activity {activity}")
                    if i < len(self.activity_ids) - 1:
                        continue
                else:
                    self.correct_activity(driver)
                    print(f"{activity} has the elevation corrected")

            # Close the browser at the end
        driver.quit()

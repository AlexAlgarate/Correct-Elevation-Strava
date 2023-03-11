from typing import List

from decouple import config
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from src.utils.logger import ErrorLogger


class CorrectElevation:
    '''
    A class to correct the elevation data of a Strava
    activity using a Selenium webdriver.

    '''

    def __init__(self, activity_ids: List[int]):
        self.activity_ids = activity_ids
        load_dotenv()
        self.email = config('EMAIL')
        self.password = config('PASSWORD')
        self.secs = 10
        self.logger = ErrorLogger()

    def get_activity_url(self, activity_id: int) -> str:
        '''
        Returns the URL of the Strava activity given an activity ID.
        '''
        return f'https://www.strava.com/activities/{activity_id}'

    def login(self, driver) -> None:
        '''
        Logs into Strava using the given Selenium webdriver.
        '''
        driver.get('https://www.strava.com/login')

        # Fill in the email and password fields
        email_field = WebDriverWait(driver, self.secs).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#email'))
        )
        email_field.send_keys(self.email)

        password_field = WebDriverWait(driver, self.secs).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))
        )
        password_field.send_keys(self.password)

        # Click on the login button
        login_button = driver.find_element(
            By.CSS_SELECTOR, 'button.btn.btn-primary'
        )
        login_button.click()

    def correct_elevation(self, driver) -> None:
        '''
        Corrects the elevation data of a Strava activity
        using the given Selenium webdriver.
        '''
        try:
            # Click on the options button
            options_button = WebDriverWait(driver, self.secs).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 'button.slide-menu.drop-down-menu.enabled.align-top'))
            )
            options_button.click()

            # Click on the correct elevation option

            correct_elevation_option = WebDriverWait(driver, self.secs).until(
                EC.presence_of_element_located((
                    By.XPATH, '/html/body/div[1]/div[3]/nav/div/button/ul/li[5]/div'))
            )
            correct_elevation_option.click()

            # Click on the button to correct the activity
            correct_activity_button = WebDriverWait(driver, self.secs).until(
                EC.presence_of_element_located((
                    By.XPATH, '/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button'))
            )
            correct_activity_button.click()

        except NoSuchElementException:
            self.logger.error(f"Correct Elevation button not found for\
                activity {driver.current_url}. Moving on to the next activity")

    def run(self) -> None:
        # Set the options that you need
        options = Options()
        options.add_argument('--start-maximized')
        options.add_experimental_option("detach", True)

        # Start the driver
        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        ) as driver:
            wait = WebDriverWait(driver, self.secs)

            # Run the log in process
            self.login(driver)

            # Correct the elevation to the activities
            for activity_id in self.activity_ids:
                activity_url = self.get_activity_url(activity_id)
                driver.get(activity_url)

                try:
                    options_button = wait.until(EC.presence_of_element_located((
                        By.CSS_SELECTOR, 'button.slide-menu.drop-down-menu.enabled.align-top'
                        ))
                    )
                    options_button.click()

                    correct_elevation_option = wait.until(EC.presence_of_element_located((
                        By.XPATH, '/html/body/div[1]/div[3]/nav/div/button/ul/li[5]/div'
                        ))
                    )
                    correct_elevation_option.click()

                    # Click on the button to correct the activity
                    correct_activity_button = wait.until(EC.presence_of_element_located((
                        By.XPATH, '/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button'
                        ))
                    )
                    correct_activity_button.click()

                    driver.implicitly_wait(15)
                except NoSuchElementException:
                    self.logger.error(f"An error {driver.current_url}")


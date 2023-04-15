from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import seconds


class ClickCorrectElevation:
    @staticmethod
    def _click_options_button(driver) -> None:
        options_button = WebDriverWait(driver, seconds).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "app-icon.icon-nav-more"))
        )
        options_button.click()

    @staticmethod
    def _click_correct_elevation_option(driver) -> None:
        correct_elevation_option = WebDriverWait(driver, seconds).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-react-class='CorrectElevation']")
            )
        )
        correct_elevation_option.click()

    @staticmethod
    def _click_correct_elevation(driver) -> None:
        # Click on the button to correct the activity
        correct_activity_button = WebDriverWait(driver, seconds).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Modal--actions--Mvyc8"))
        )
        correct_activity_button.click()
        # @staticmethod
        # def _click_correct_elevation(driver) -> None:
        #     # Click on the button to correct the activity
        #     correct_activity_button = WebDriverWait(driver, seconds).until(
        #         EC.element_to_be_clickable(
        #             (
        #                 By.XPATH,
        #                 "/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button"
        #             )
        #         )
        #     )
        #     correct_activity_button.click()

        driver.implicitly_wait(15)

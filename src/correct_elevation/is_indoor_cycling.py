from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import seconds


class IndoorCycling:
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

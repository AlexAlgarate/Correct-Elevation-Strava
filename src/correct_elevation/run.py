from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.correct_elevation.correct_activity import ClickCorrectElevation
from src.correct_elevation.get_activity_url import GetACtivityURL
from src.correct_elevation.is_indoor_cycling import IndoorCycling
from src.correct_elevation.login_strava import LoginStrava


class CorrectElevation:
    def __init__(self, id_activity: List[int]) -> None:
        self.id_activity = id_activity
        self.url = GetACtivityURL()
        self.login = LoginStrava()
        self.indoor_cycling = IndoorCycling()
        self.click_correct = ClickCorrectElevation()

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

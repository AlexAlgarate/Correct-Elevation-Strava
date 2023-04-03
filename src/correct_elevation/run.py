import time
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
        # Set the options that you need
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        # Start the driver
        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        ) as driver:

            # Run the log in process
            self.login.login(driver)
            for i, activity in enumerate(self.id_activity):
                print(f"\n############## \nProcessing activity {activity}\n")

                activity_url = self.url.get_activity_url(activity)
                driver.get(activity_url)
                print(f"\n###### \nActivity: {activity}\n")
                time.sleep(2)
                if self.indoor_cycling._is_activity_indoor_cycling(driver):
                    print(f"\n##\nDetected indoor cycling activity {activity}")
                    if i < len(self.id_activity) - 1:
                        continue
                else:
                    self.click_correct._click_options_button(driver)
                    self.click_correct._click_correct_elevation_option(driver)
                    print("HA CLICADO EN CORRECT")
                    self.click_correct._click_correct_elevation(driver)
                    # self.correct_activity(driver)
                    print(f"\nElevation has corrected for activity:{activity}")

            # Close the browser at the end
        driver.quit()

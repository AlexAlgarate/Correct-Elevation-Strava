from config import PASSWORD, EMAIL
from src.correct_elevation.credentials import Credentials
from config import seconds
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.correct_elevation.strava import Strava


from logger.logger import ErrorLogger, InfoLogger


info_logger = InfoLogger()
error_logger = ErrorLogger()


def main():
    try:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        with webdriver.Chrome(
                service=Service(
                    ChromeDriverManager().install()),
                options=options
        ) as driver:

            credentials = Credentials(EMAIL, PASSWORD)
            strava = Strava(driver)

            for strava_activity in strava.login(credentials).get_latest_activities():
                strava_activity.correct_elevation()

        driver.implicitly_wait(seconds)
        driver.quit()

        info_logger.info(f"{id} has corrected.")
    except Exception as e:
        error_logger.error(f"Error: {e} in '{__name__}'")


if __name__ == '__main__':
    main()

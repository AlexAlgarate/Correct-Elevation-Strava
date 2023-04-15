# from config import PASSWORD, EMAIL
# from src.correct_elevation.credentials import Credentials
# from config import seconds
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# from src.correct_elevation.strava import Strava
from src.strava_API.StravaFetcher import StravaFetcher
from logger.logger import ErrorLogger, InfoLogger
from src.strava_API.ids_to_correct import GetActivities
from src.strava_API.access_token import GetAccessToken

info_logger = InfoLogger()
error_logger = ErrorLogger()

# def main():
#     try:
#         options = Options()
#         options.add_argument("--start-maximized")
#         options.add_experimental_option("detach", True)

#         with webdriver.Chrome(
#                 service=Service(
#                     ChromeDriverManager().install()),
#                 options=options
#         ) as driver:

#             credentials = Credentials(EMAIL, PASSWORD)
#             strava = Strava(driver)

#             for strava_activity in strava.login(credentials).get_latest_activities():
#                 strava_activity.correct_elevation()

#         driver.implicitly_wait(seconds)
#         driver.quit()

#         info_logger.info(f"{id} has corrected.")
#     except Exception as e:
#         error_logger.error(f"Error: {e} in '{__name__}'")


# if __name__ == '__main__':
#     main()


def main():

    # def get_latest_activities(self, limit: int = 10) -> List[StravaActivity]:
    try:
        access_token = GetAccessToken().get_strava_access_token()
        summary_of_activities = GetActivities(access_token)
        strava_fetcher = StravaFetcher(summary_of_activities).filtered_dataframe()
        info_logger.info(strava_fetcher)

        # return [StravaActivity(self.driver, activity_id) for activity_id in filtered_activities[limit:]]
    except Exception as e:
        # error_logger.error(f"Error: {e} in '{__name__}'")
        error_logger.error(f"The error was: {e}")


if __name__ == "__main__":
    main()

# from src.utils.ids_to_correct import StravaFetcher, SummaryOfActivities
# from src.correct_elevation.correct_elevation import CorrectElevation
from src.utils.access_token import GetAccessToken
from src.utils.logger import InfoLogger, ErrorLogger
# from src.utils.generate_credentials import GenerateAccessToken
# from src.correct_elevation.run import CorrectElevation


def main():
    info_logger = InfoLogger()
    error_logger = ErrorLogger()

    a = GetAccessToken().get_strava_access_token()
    info_logger.info(f"{a}")
    # try:
    #     summary_of_activities = SummaryOfActivities()
    #     strava_fetcher = StravaFetcher(summary_of_activities)
    #     filtered_activities = strava_fetcher.fetch_activities_summary()
    #     info_logger.info(filtered_activities)
    # except Exception as e:
    #     error_logger.error(f"Error: {e} in '{__name__}'")

    #####################
    # ids_to_correct = StravaFetcher().fect_activities_summary()
    # print(ids_to_correct)
    # id = [8040982449, 7950538016,6884837423, 7934530628]
    # id = [6884837423]
    # try:

    #     id = [8040982449]
    #     correct_elevation = CorrectElevation(id)
    #     correct_elevation.run()

    #     info_logger.info(f"{id} has corrected.")
    # except Exception as e:
    #     error_logger.error(f"Error: {e} in '{__name__}'")


if __name__ == '__main__':
    main()

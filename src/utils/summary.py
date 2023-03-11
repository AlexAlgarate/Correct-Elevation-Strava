import pandas as pd
from pandas import json_normalize
import requests
from src.utils.access_token_env import AccessToken
from src.utils.logger import ErrorLogger
from typing import List


class Summary:

    API_URL: str = 'https://www.strava.com/api/v3/activities'
    PAGE_SIZE: str = '200'

    def __init__(self) -> None:
        '''
        Initializes a new Summary object.
        '''
        # self.summary_data: pd.DataFrame = pd.DataFrame()
        self.access_token: str = AccessToken().get_access_token()
        self.logger = ErrorLogger()

    def _get_activities(self, page: int) -> List[dict]:
        '''
        Set the request to the API.

        Results:
            The response from the API in a JSON format.
        '''
        try:
            response = requests.get(
                self.API_URL,
                params={
                    'access_token': self.access_token,
                    'per_page': self.PAGE_SIZE,
                    'page': page
                }
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Error: {e}. HHTTP error has occurred.")
            raise
        except requests.exceptions.ConnectTimeout as e:
            self.logger.error(f"Error: {e}. A TimeOut error has occurred.")
            raise
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Error: {e}. Cannot connect to the server.")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error: {e}. Other kind of error has occurred.")
            raise

    def _get_all_activities(self) -> List[dict]:
        '''
        Makes a GET request to the Strava API for fetching all activities
        by iterating over all available pages in your profile.

        Returns:
            a list of activities in JSON format
        '''
        all_activities: List[dict] = []
        page: int = 1

        while True:
            activities = self._get_activities(page)

            if not activities:
                break

            all_activities.extend(activities)
            page += 1

        return all_activities

    def fetch_ids_data(self) -> pd.DataFrame:
        '''
        Fetches all activities from Strava and normalizes the data
        to create a summary of the user's activities.

        Returns:

        '''
        activities = self._get_all_activities()
        df = json_normalize(activities)
        df_ids = self.get_ids_to_correct(df)
        return df_ids

    def get_ids_to_correct(self, df):
        ids_to_correct_elevation = df.loc[
            (df['sport_type'].isin(['Ride', 'Run']))
            &
            (df['total_elevation_gain'] == 0)
        ]['id'].to_list()
        return ids_to_correct_elevation

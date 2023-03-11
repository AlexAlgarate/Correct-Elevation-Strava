import os
import time
from typing import Optional, Union

import requests
from dotenv import find_dotenv, set_key

from src.utils.load_env_var import Env
from src.utils.credentials_env import Credentials
from src.utils.logger import ErrorLogger, WarningLogger


class RefreshTokenManager:

    '''
    A class to manage the refreshing proccess of the access token.
    Other file uses this class to check if the access token has expired and
    if check_expired method returns True, it uses the refreshing_token method
    to make a POST request to the Strava API.
    Finally, this class uses another method to save the new credentials in the
    .env file.
    '''

    TOKEN_URL: str = 'https://www.strava.com/oauth/token'
    REFRESH_TOKEN_TYPE = 'refresh_token'
    ENV_FILE = find_dotenv()

    def __init__(self) -> None:

        self.new_credentials = Credentials()
        self.logger_error = ErrorLogger()
        self.logger_warning = WarningLogger()

        # Load environment variables
        env = Env()
        self.client_id = env.get_client_id()
        self.secret_key = env.get_secret_key()
        self.refresh_token = env.get_refresh_token()
        self.expires_at = env.get_expires_at()

    def check_expired(self) -> bool:

        '''
        Returns 'True' if the expiration date of the acess token is less than
        the current time.
        Returns 'False' otherwise.
        '''
        if self.expires_at is None:
            return False

        if not isinstance(self.expires_at, int):
            self.logger_warning.warning('Expires_at should be an integer')
            return False

        return self.expires_at < time.time()

    def refresh_access_token(self) -> str:

        '''
        Refreshes the access token by making a call to the Strava API and
        saves the new credentials in the .env file.
        '''
        # Set the URL to make the request

        # Set the params of the request
        token_data: dict[str, Union[str, int]] = {
            'client_id': self.client_id,
            'client_secret': self.secret_key,
            'grant_type': self.REFRESH_TOKEN_TYPE,
            'refresh_token': self.refresh_token
        }
        try:
            refresh_response = requests.post(
                url=self.TOKEN_URL,
                data=token_data
            )
            # Raise an exception if the response is not ok
            refresh_response.raise_for_status()
            refresh_response_data = refresh_response.json()

            access_token: str = refresh_response_data['access_token']
            refresh_token: str = refresh_response_data['refresh_token']
            expires_at: int = int(refresh_response_data['expires_at'])

            self._update_env(access_token, refresh_token, expires_at)
            return access_token

        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error has occurred while\
                making the request to the API: {e}")

            self.new_credentials.get_credentials()
            access_token: str = os.getenv('ACCESS_TOKEN')
            return access_token

    def _update_env(
        self,
        access_token: str,
        refresh_token: str,
        expires_at: Optional[int]
    ) -> None:

        '''
        Update the access token and expires_at in the .env file.
        '''
        try:

            set_key(self.ENV_FILE, 'ACCESS_TOKEN', access_token)
            set_key(self.ENV_FILE, 'REFRESH_TOKEN', refresh_token)
            if expires_at is not None:
                set_key(self.ENV_FILE, 'EXPIRES_AT', str(expires_at))

        except Exception as e:
            self.logger_error.error(
                f"An error has occurred while updating the .env file: {e}"
            )

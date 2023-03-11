import os

from dotenv import load_dotenv

from src.utils.credentials_env import Credentials
from src.utils.logger import ErrorLogger
from src.utils.refresh_token_env import RefreshTokenManager


class AccessToken:

    """
    A class that manages access tokens for API requests.

    Attributes:
        - refresh (RefreshTokenManager): an instance of the RefreshTokenManager
        class to handle token refreshing.
        - _new_credentials (Credentials): an instance of the Credentials class
        to handle getting new credentials from the API.
        - _logger (ErrorLogger): an instance of the ErrorLogger class
        to handle logging errors.
    """

    def __init__(self) -> None:
        self.refresh = RefreshTokenManager()
        self._new_credentials = Credentials()
        self._logger = ErrorLogger()
        load_dotenv()

    def get_access_token(self) -> str:

        '''
        Return the access token from the .env file.
        Firstly, check if the access token has expired or not.
        If it has expired, it gets a new access token.
        Otherwise, it returns the last access token that is available
        in the .env file.
        If there are some kind of error, it gets new credentials and
        a new access token.
        '''
        if self._access_token_has_expired():
            self._refresh_the_access_token()

        try:
            access_token = self._get_access_token_from_env()
            return access_token
        except FileNotFoundError as e:
            self._logger.error(f"Error:{e}. Credentials not found")
            raise
        except KeyError as e:
            self._logger.error(
                f"Error: {e}. ACCESS_TOKEN not found in the .env file"
            )
        except Exception as e:
            self._logger.error(f"An error has occurred: {e}")
            self._get_new_credentials()
            access_token = self._get_access_token_from_env()
            return access_token

    def _access_token_has_expired(self) -> bool:
        '''
        Check if the access token has expired or not
        '''
        return self.refresh.check_expired()

    def _refresh_the_access_token(self) -> None:
        '''
        Refresh the access token
        '''
        self._logger.info(
            "The access token has expired..."
            "You'll be redirected to the oauth page to get a new access token"
        )
        self.refresh.refresh_access_token()

    def _get_access_token_from_env(self) -> str:
        '''
        Get the access token from the environment variables
        '''
        access_token = os.getenv('ACCESS_TOKEN')
        return access_token

    def _get_new_credentials(self) -> None:
        '''
        Get new credentials from the API and update the environment variables.
        '''
        self._new_credentials.get_credentials()

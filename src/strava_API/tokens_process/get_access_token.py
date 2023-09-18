import os

from decouple import UndefinedValueError
from dotenv import load_dotenv

from config import access_token_env
from logger.logger import ErrorLogger, InfoLogger
from src.strava_api.tokens_process.generate_credentials import GenerateAccessToken
from src.strava_api.tokens_process.refresh_token import RefreshTokenManager

error_logger = ErrorLogger()
info_logger = InfoLogger()


class GetAccessToken:
    refresh: RefreshTokenManager = RefreshTokenManager()

    """
        Return the access token from the .env file.
        Firstly, check if the access token has expired or not.
        If it has expired, it gets a new access token.
        Otherwise, it returns the last access token that is available
        in the .env file.
        If there are some kind of error, it gets new credentials and
        a new access token.

    Attributes:
        - refresh (RefreshTokenManager): an instance of the RefreshTokenManager
        class to handle token refreshing.
    """

    # def __init__(self) -> None:
    #     self.refresh = RefreshTokenManager()

    def get_access_token(self) -> str:
        """
        Get the access token value from the .env to use the Strava API

        """
        try:
            if self._access_token_has_expired():
                new_access_token: str = self._refresh_the_access_token()
                os.environ[access_token_env] = new_access_token
                # os.environ["STRAVA_ACCESS_TOKEN"] = new_access_token
            new_access_token = os.getenv(access_token_env)
            # new_access_token = os.getenv("STRAVA_ACCESS_TOKEN")
            if new_access_token is None:
                raise UndefinedValueError("Access token not found in the .env")

            return new_access_token

        except UndefinedValueError:
            error_logger.error("Access token not found in the .env")
            self._get_new_access_token()
            access_token = self._get_access_token_from_env()
            info_logger.info("Access token retrieved from the .env file")
            return access_token

    def _access_token_has_expired(self) -> bool:
        """
        It checks if the access token has expired or not

        Returns:
            bool: True if the access token has expired, False otherwise

        """

        return self.refresh._check_expired()

    def _refresh_the_access_token(self) -> str:
        """
        Refresh the access token.

        Returns:
            str: A new access token string
        """

        info_logger.info("The access token has expired. Refreshing the access token...")
        access_token = self.refresh.refresh_access_token()
        info_logger.info("Access token refreshed successfully")
        return access_token

    def _get_access_token_from_env(self) -> str:
        """
        Get the access token from the environment variables

        Returns:
            str: The access token from the environment variables

        """
        load_dotenv()
        access_token_from_env: str = os.getenv(access_token_env)
        # access_token_from_env = os.getenv("STRAVA_ACCESS_TOKEN")
        if access_token_from_env:
            return access_token_from_env
        else:
            raise UndefinedValueError("ACCESS_TOKEN not found in the env file")

    def _get_new_access_token(self) -> None:
        """
        Get new credentials from the API and update the environment variables.

        """

        info_logger.info("Getting new credentials from the Strava API")
        credentials_handler = GenerateAccessToken()
        credentials_handler.generate_access_token()
        info_logger.info("Credentials updated successfully")

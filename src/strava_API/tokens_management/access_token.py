import os

from decouple import UndefinedValueError
from dotenv import load_dotenv

from src.strava_API.tokens_management.generate_credentials import GenerateAccessToken
from logger.logger import ErrorLogger, InfoLogger
from src.strava_API.tokens_management.refresh_token import RefreshTokenManager


class GetAccessToken:
    refresh: RefreshTokenManager
    logger_error: ErrorLogger
    logger_info: InfoLogger

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
        - _new_credentials (Credentials): an instance of the Credentials class
        to handle getting new credentials from the API.
        - logger (ErrorLogger): an instance of the ErrorLogger class
        to handle logging errors.

    """

    def __init__(self) -> None:
        self.refresh = RefreshTokenManager()
        self.logger_error = ErrorLogger()
        self.logger_info = InfoLogger()

    def get_access_token(self) -> str:
        """
        Get the access token value from the .env to use the Strava API

        """
        try:
            if self._access_token_has_expired():
                new_access_token = self._refresh_the_access_token()
                os.environ["STRAVA_ACCESS_TOKEN"] = new_access_token
            new_access_token = os.getenv("STRAVA_ACCESS_TOKEN")
            if new_access_token is None:
                raise UndefinedValueError("Access token not found in the .env")

            return new_access_token

        except UndefinedValueError:
            self.logger_error.error("Access token not found in the .env")
            self._get_new_access_token()
            access_token = self._get_access_token_from_env()
            self.logger_info.info("Access token retrieved from the .env file")
            return access_token

    def _access_token_has_expired(self) -> bool:
        """
        Check if the access token has expired or not

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

        self.logger_info.info(
            "The access token has expired. Refreshing the access token..."
        )
        access_token = self.refresh._refresh_access_token()
        return access_token
        # self.logger_info.info("Access token refreshed successfully")

    def _get_access_token_from_env(self) -> str:
        """
        Get the access token from the environment variables

        Returns:
            str: The access token from the environment variables

        """
        load_dotenv()
        access_token_from_env = os.getenv("STRAVA_ACCESS_TOKEN")
        if access_token_from_env:
            return access_token_from_env
        else:
            raise UndefinedValueError("ACCESS_TOKEN not found in the env file")

    def _get_new_access_token(self) -> None:
        """
        Get new credentials from the API and update the environment variables.

        """

        self.logger_info.info("Getting new credentials from the Strava API")
        credentials_handler = GenerateAccessToken()
        credentials_handler.generate_access_token()
        self.logger_info.info("Credentials updated successfully")

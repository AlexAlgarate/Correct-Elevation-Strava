from decouple import UndefinedValueError
from dotenv import load_dotenv

from config import ACCESS_TOKEN
from src.utils.generate_credentials import GenerateAccessToken
from src.utils.logger import ErrorLogger, InfoLogger
from src.utils.refresh_token import RefreshTokenManager


class GetAccessToken:

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

    def get_strava_access_token(self) -> str:

        """
        Get the access token value from the .env to use the Strava API

        """

        if self._access_token_has_expired():
            self._refresh_the_access_token()

        try:
            acces_token = self._get_access_token_from_env()
            self.logger_info.info("Access token retrieved from the .env file")
            return acces_token

        except UndefinedValueError:
            self.logger_error.error("Access token not found in the .env")
            self._get_new_access_token()
            acces_token = self._get_access_token_from_env()
            self.logger_info.info("Access token retrieved from the .env file")
            return acces_token

    def _access_token_has_expired(self) -> bool:

        """
        Check if the access token has expired or not

        Returns:
            bool: True if the access token has expired, False otherwise

        """

        return self.refresh._check_expired()

    def _refresh_the_access_token(self) -> None:

        """
        Refresh the access token.

        """

        self.logger_info.info("The access token has expired."
                              "Refreshing the access token...")
        self.refresh._refresh_access_token()
        self.logger_info.info("Access token refreshed successfully")

    def _get_access_token_from_env(self) -> str:

        """
        Get the access token from the environment variables

        Returns:
            str: The access token from the environment variables

        """

        load_dotenv()
        access_token_from_env = ACCESS_TOKEN
        if access_token_from_env:
            return access_token_from_env
        else:
            raise UndefinedValueError(
                "ACCESS_TOKEN not found in the .env file"
            )

    def _get_new_access_token(self) -> None:

        """
        Get new credentials from the API and update the environment variables.

        """

        self.logger_info.info("Getting new credentials from the Strava API")
        credentials_handler = GenerateAccessToken()
        credentials_handler.get_access_token()
        self.logger_info.info("Credentials updated successfully")

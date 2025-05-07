import os

from dotenv import load_dotenv

from src.strava_API.tokens_process.refresh_token import RefreshTokenManager
from src.strava_API.tokens_process.request_credentials import RequestAccessToken
from utils import config, err_log, exc_log


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
        refresh (RefreshTokenManager): an instance of the RefreshTokenManager
        class to handle token refreshing.
    """

    def get_access_token(self) -> str:
        """
        Get the access token value from the .env to use the Strava API
        """

        try:
            access_token: str = os.getenv(config.access_token_env)

            if access_token is None:
                err_log.error(
                    "Access token has not found in the .env. Getting a new one..."
                )
                self._get_new_access_token()

            if self._access_token_has_expired():
                refreshed_access_token: str = self._refresh_the_access_token()
                os.environ[config.access_token_env] = refreshed_access_token
            refreshed_access_token = os.getenv(config.access_token_env)
            if refreshed_access_token is None:
                err_log.error("Access token not found in the .env")

            return refreshed_access_token

        except (ValueError, Exception, TypeError) as e:
            exc_log.exception(e)
            self._get_new_access_token()
            new_access_token: str = self._get_access_token_from_env()
            print(f"The acccess token has retrieved successfully: {new_access_token}")
            return new_access_token

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
        access_token: str = self.refresh.refresh_access_token()
        return access_token

    def _get_access_token_from_env(self) -> str:
        """
        Get the access token from the environment variables

        Returns:
            str: The access token from the environment variables
        """
        try:
            load_dotenv()
            access_token: str = os.getenv(config.access_token_env)
            if not access_token:
                return self._get_new_access_token()
            return access_token
        except Exception as e:
            exc_log.exception(e)

    def _get_new_access_token(self) -> None:
        """
        Get new credentials from the API and update the environment variables.
        """
        print("Getting new credentials from the Strava API")
        load_dotenv()
        credentials_handler = RequestAccessToken()
        credentials_handler.generate_access_token()
        print("Credentials updated successfully")
        access_token: str = os.getenv(config.access_token_env)
        return access_token

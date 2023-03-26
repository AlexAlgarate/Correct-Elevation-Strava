import os

from dotenv import load_dotenv

from src.utils.logger import ErrorLogger


class LoadEnvironmentVariables:

    def __init__(self) -> None:
        load_dotenv()
    """
    It loads the environment variables.

    """

    def get_client_id(self) -> int:
        return int(os.getenv("STRAVA_CLIENT_ID")) or \
            ValueError("Missing CLIENT_ID environment variable")

    def get_engine_database(self) -> str:
        return os.getenv("POSTGRES_ENGINE") or \
            ValueError("Missing ENGINE environment variable")

    def get_secret_key(self) -> str:
        return os.getenv("STRAVA_SECRET_KEY") or \
            ValueError("Missing SECRET_KEY environment variable")

    def get_refresh_token(self) -> str:
        return os.getenv("STRAVA_REFRESH_TOKEN") or \
            ValueError("Missing REFRESH_TOKEN environment variable")

    def get_access_token(self) -> str:
        return os.getenv("STRAVA_ACCESS_TOKEN") or \
            ValueError("Missing ACCESS_TOKEN environment variable")

    def strava_email(self) -> str:
        return os.getenv("STRAVA_EMAIL") or \
            ValueError("Missing EMAIL environment variable")

    def strava_password(self) -> str:
        return os.getenv("STRAVA_PASSWORD") or \
            ValueError("Missing ACCESS_TOKEN environment variable")

    def get_expires_at(self) -> int:
        expires_at = os.getenv("STRAVA_EXPIRES_AT")
        if expires_at is None:
            return None
        try:
            return int(expires_at)
        except ValueError:
            ErrorLogger().error(
                "Invalid value for EXPIRES_AT environment variable"
            )
            return None

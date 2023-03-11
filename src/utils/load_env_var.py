import os

from dotenv import load_dotenv

from src.utils.logger import ErrorLogger


class Env:

    def __init__(self) -> None:
        load_dotenv()
    '''
    It loads the environment variables that are neccessary in the getting
    credentials proccess.
    '''

    def get_client_id(self) -> int:
        return int(os.getenv('CLIENT_ID')) or \
            ValueError("Missing CLIENT_ID environment variable")

    def get_engine_database(self) -> str:
        return os.getenv('ENGINE_DATABASE') or \
            ValueError("Missing CLIENT_ID environment variable")

    def get_secret_key(self) -> str:
        return os.getenv('SECRET_KEY') or \
            ValueError("Missing SECRET_KEY environment variable")

    def get_refresh_token(self) -> str:
        return os.getenv('REFRESH_TOKEN') or \
            ValueError("Missing REFRESH_TOKEN environment variable")

    def get_access_token(self) -> str:
        return os.getenv('ACCESS_TOKEN') or \
            ValueError("Missing ACCESS_TOKEN environment variable")

    def get_expires_at(self) -> int:
        expires_at = os.getenv('EXPIRES_AT')
        if expires_at is None:
            return None
        try:
            return int(expires_at)
        except ValueError:
            ErrorLogger().error(
                "Invalid value for EXPIRES_AT environment variable"
            )
            return None

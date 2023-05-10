import os
from typing import Dict, Union

from dotenv import find_dotenv, load_dotenv

from logger.logger import ErrorLogger


logger = ErrorLogger()

# Load environment variables


try:
    load_dotenv()
    client_id_env: str = "STRAVA_CLIENT_ID"
    secret_key_env: str = "STRAVA_SECRET_KEY"
    engine_env: str = "POSTGRES_ENGINE"
    email_env: str = "STRAVA_EMAIL"
    password_env: str = "STRAVA_PASSWORD"
    access_token_env: str = "STRAVA_ACCESS_TOKEN"
    refresh_token_env: str = "STRAVA_REFRESH_TOKEN"
    expires_at_env: str = "STRAVA_EXPIRES_AT"

    ENGINE: str = os.getenv(engine_env)
    EMAIL: str = os.getenv(email_env)
    PASSWORD: str = os.getenv(password_env)
    CLIENT_ID: int = int(os.getenv(client_id_env))
    SECRET_KEY: str = os.getenv(secret_key_env)
    ACCESS_TOKEN: str = os.getenv(access_token_env)
    REFRESH_TOKEN: str = os.getenv(refresh_token_env)
    EXPIRES_AT: int = os.getenv(expires_at_env)

except KeyError as e:
    logger.error(f"Error trying to load the environment variable: {e}")

# Load other variables
try:
    token_url: str = "https://www.strava.com/oauth/token"
    refresh_token_grant_type: str = "refresh_token"
    redirect_url: str = "http://localhost/exchange_token"
    authorization_url: str = "https://www.strava.com/oauth/authorize"
    scopes: str = "read,read_all,activity:read,activity:read_all"
    api_url: str = "https://www.strava.com/api/v3/activities"
    page_size: str = "200"
    dot_env_file = find_dotenv()
    header_code_OAuth: Dict[str, Union[int, str]] = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_url,
        "approval_prompt": "force",
        "scope": scopes
    }
    seconds = 10
    url_to_get_OAuth_code: str = f"{authorization_url}?client_id={CLIENT_ID}&response_type=code&redirect_uri={redirect_url}&approval_prompt=force&scope={scopes}"
    refresh_data: Dict[str, Union[str, int]] = {
        "client_id": CLIENT_ID,
        "client_secret": SECRET_KEY,
        "grant_type": refresh_token_grant_type,
        "refresh_token": REFRESH_TOKEN
    }

except KeyError as e:
    logger.error(f"Error trying to load the variable: {e}")

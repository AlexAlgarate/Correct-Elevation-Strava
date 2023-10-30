import os
from typing import Dict, List, Union

from dotenv import find_dotenv, load_dotenv

from utils.logger import exception_logger as exc_log

try:
    load_dotenv()
    client_id_env: str = "STRAVA_CLIENT_ID"
    secret_key_env: str = "STRAVA_SECRET_KEY"
    email_env: str = "STRAVA_EMAIL"
    password_env: str = "STRAVA_PASSWORD"
    access_token_env: str = "STRAVA_ACCESS_TOKEN"
    refresh_token_env: str = "STRAVA_REFRESH_TOKEN"
    expires_at_env: str = "STRAVA_EXPIRES_AT"

    EMAIL: str = os.getenv(email_env)
    PASSWORD: str = os.getenv(password_env)
    CLIENT_ID: int = int(os.getenv(client_id_env))
    SECRET_KEY: str = os.getenv(secret_key_env)
    ACCESS_TOKEN: str = os.getenv(access_token_env)
    REFRESH_TOKEN: str = os.getenv(refresh_token_env)
    EXPIRES_AT: int = os.getenv(expires_at_env)

except KeyError as e:
    exc_log.exception(f"Error trying to load the environment variable: {e}")

# Load other variables
try:
    token_url: str = "https://www.strava.com/oauth/token"
    grant_type_refresh_token: str = "refresh_token"
    redirect_url: str = "http://localhost/exchange_token"
    authorization_url: str = "https://www.strava.com/oauth/authorize"
    scopes: str = "read,read_all,activity:read,activity:read_all"
    api_url: str = "https://www.strava.com/api/v3/activities"
    page_size: str = "200"
    dot_env_file = find_dotenv()
    seconds = 2

    client_id: str = f"client_id={CLIENT_ID}"
    redirect_uri: str = f"redirect_uri={redirect_url}"
    response_type: str = "response_type=code"
    approval_prompt: str = "approval_prompt=force"
    scope: str = f"scope={scopes}"

    OAuth_url: str = (
        f"{authorization_url}?{client_id}&{response_type}&{redirect_uri}&{approval_prompt}&{scope}"
    )

    refresh_data: Dict[str, Union[str, int]] = {
        "client_id": CLIENT_ID,
        "client_secret": SECRET_KEY,
        "grant_type": grant_type_refresh_token,
        "refresh_token": REFRESH_TOKEN,
    }
    url_login_strava: str = "https://www.strava.com/login"

    meters_elevation_gain: int = 0
    elevation_column: str = "total_elevation_gain"
    id_activity_column: str = "id"
    sports_to_correct: List[str] = ["Ride", "Run"]
    sports_column: str = "sport_type"

except KeyError as e:
    exc_log.exception(f"Error trying to load the variable: {e}")

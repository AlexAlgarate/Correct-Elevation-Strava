import json
import re
import webbrowser
from typing import Any, Dict, Union

import requests
from dotenv import load_dotenv, set_key
from requests import Request
from decouple import config
# from src.utils.load_env_var import Env
from src.utils.logger import ErrorLogger


class OAuthCode:
    """
    Class for handling the authentication process with Strava API.

    """

    REDIRECT_URL: str = "http://localhost/exchange_token"
    AUTHORIZATION_URL: str = "https://www.strava.com/oauth/authorize"
    SCOPES: str = "read,read_all,activity:read,activity:read_all"

    def __init__(self) -> None:
        # Set the logger that captures any error that occurres
        self.logger = ErrorLogger()
        # env = Env()
        self.client_id = config("CLIENT_ID")
        # self.client_id = env.get_client_id()

    def get_oauth_code(self) -> str:
        """
        Launches a web browser to retrieve the Oauth code from Strava.

        """
        header: Dict[str, Union[int, str]] = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URL,
            "approval_prompt": "force",
            "scope": self.SCOPES
        }

        try:
            get_url_code = Request(
                "GET",
                self.AUTHORIZATION_URL,
                params=header
            ).prepare()
            webbrowser.open(get_url_code.url)
            url_with_code = input().strip()
            print("Paste here the URL from the browser: ", end="")

            code_pattern = re.compile("&code=([\a-z]+)&")
            code: str = code_pattern.findall(url_with_code)[0]
            return code

        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error has occurred while making\
                the request: {e}")
            raise


class Credentials:
    URL_TOKEN: str = "https://www.strava.com/oauth/token"

    def __init__(self) -> None:
        # env = Env()
        self.client_id = config("CLIENT_ID")
        self.secret_key = config("SECRET_KEY")
        # self.client_id = env.get_client_id()
        # self.secret_key = env.get_secret_key()
        self.code = OAuthCode()
        self.logger = ErrorLogger()
        load_dotenv()

    def get_credentials(self) -> None:
        """
        Gets the credentials (access_token, refresh_token, and expires_at)
        received from the API making a POST request.
        Finally, these credentials are stored in an .env file
        using the set_key function.
        """
        try:
            # Set the data required for the POST request
            data: Dict[str, Union[str, int]] = {
                    "client_id": self.client_id,
                    "client_secret": self.secret_key,
                    "code": self.code.get_oauth_code(),
                    "grant_type": "authorization_code"
                    }

            response = requests.post(url=self.URL_TOKEN, data=data).json()
            # response.raise_for_status()
            # response_credentials = response.json()

            access_token: str = response["access_token"]
            refresh_token: str = response["refresh_token"]
            expires_at: str = response["expires_at"]

            # set_key(".env", "ACCESS_TOKEN", access_token)
            # set_key(".env", "REFRESH_TOKEN", refresh_token)
            # set_key(".env", "EXPIRES_AT", str(expires_at))

            with open(".env", "a") as f:
                f.write(f"\nACCESS_TOKEN={access_token}")
                f.write(f"\nREFRESH_TOKEN={refresh_token}")
                f.write(f"\nEXPIRES_AT={expires_at}")

        # If there are any exception, it will be stored in a log file
        except (
            requests.exceptions.RequestException,
            KeyError,
            json.JSONDecodeError
        ) as e:
            self.logger.error(f"An error has ocurred while\
                requesting credentials:\n {e}")
            raise
# class Credentials:
#     """
#     Class for handling the authentication process with Strava API.
#     """

#     REDIRECT_URL: str = "http://localhost/exchange_token"
#     AUTHORIZATION_URL: str = "https://www.strava.com/oauth/authorize"
#     SCOPES: str = "read,read_all,activity:read,activity:read_all"
#     URL_TOKEN: str = "https://www.strava.com/oauth/token"

#     def __init__(self) -> None:
#         """
#         Initializes the Credentials object.
#         """
#         # Set the logger that captures any error that occurres
#         self.logger = ErrorLogger()
#         env = Env()
#         self.client_id = env.get_client_id()
#         self.secret_key = env.get_secret_key()

#     def get_oauth_code(self) -> str:
#         """
#         Launches a web browser to retrieve the Oauth code from Strava.
#         """
#         header: Dict[str, Union[int, str]] = {
#             "client_id": self.client_id,
#             "response_type": "code",
#             "redirect_uri": self.REDIRECT_URL,
#             "approval_prompt": "force",
#             "scope": self.SCOPES
#         }

#         try:
#             code_request = Request(
#                 "GET",
#                 self.AUTHORIZATION_URL,
#                 params=header
#             ).prepare()
#             webbrowser.open(code_request.url)
#             print("Paste here the URL from the browser: ", end="")
#             raw_url: str = input().strip()

#             code_pattern = re.compile("&code=([\a-z]+)&")
#             code: str = code_pattern.findall(raw_url)[0]
#             return code

#         except requests.exceptions.RequestException as e:
#             self.logger.error(f"An error has occurred while making\
#                 the request: {e}")
#             raise

#     def get_credentials(self) -> None:
#         """
#         Gets the credentials (access_token, refresh_token, and expires_at)
#         received from the API making a POST request.
#         Finally, these credentials are stored in an .env file
#         using the set_key function.
#         """
#         try:
#             # Set the data required for the POST request
#             data: Dict[str, Union[str, int]] = {
#                     "client_id": self.client_id,
#                     "client_secret": self.secret_key,
#                     "code": self.get_oauth_code(),
#                     "grant_type": "authorization_code"
#                     }

#             response: Dict[str, Any] = requests.post(
#                 url=self.URL_TOKEN,
#                 data=data
#             )

#             response.raise_for_status()

#             response_credentials = response.json()

#             access_token: str = response_credentials["access_token"]
#             refresh_token: str = response_credentials["refresh_token"]
#             expires_at: str = response_credentials["expires_at"]

#             set_key(".env", "ACCESS_TOKEN", access_token)
#             set_key(".env", "REFRESH_TOKEN", refresh_token)
#             set_key(".env", "EXPIRES_AT", str(expires_at))

#         # If there are any exception, it will be stored in a log file
#         except (
#             requests.exceptions.RequestException,
#             KeyError,
#             json.JSONDecodeError
#         ) as e:
#             self.logger.error(f"An error has ocurred while\
#                 requesting credentials:\n {e}")
#             raise

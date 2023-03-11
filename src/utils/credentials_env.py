import json
import re
import webbrowser
from typing import Any, Dict, Union

import requests
from dotenv import set_key
from requests import Request

from src.utils.load_env_var import Env
from src.utils.logger import ErrorLogger


class Credentials:
    '''
    Class for handling the authentication process with Strava API.
    '''

    AUTHORIZATION_URL: str = 'https://www.strava.com/oauth/authorize'
    REDIRECT_URL: str = 'http://localhost/exchange_token'
    SCOPES: str = 'read,read_all,activity:read,activity:read_all'
    URL_TOKEN: str = 'https://www.strava.com/oauth/token'

    def __init__(self) -> None:
        '''
        Initializes the Credentials object.
        '''
        # Set the logger that captures any error that occurres
        self.logger = ErrorLogger()
        env = Env()
        self.client_id = env.get_client_id()
        self.secret_key = env.get_secret_key()

    def get_oauth_code(self) -> str:
        '''
        Launches a web browser to retrieve the Oauth code from Strava.
        '''
        header: Dict[str, Union[int, str]] = {
            'client_id': self.env.get_client_id(),
            'response_type': 'code',
            'redirect_uri': self.REDIRECT_URL,
            'approval_prompt': 'force',
            'scope': self.SCOPES
        }

        try:
            code_request = Request(
                'GET',
                self.AUTHORIZATION_URL,
                params=header
            ).prepare()
            webbrowser.open(code_request.url)
            print('Paste here the URL from the browser: ', end='')
            raw_url: str = input().strip()

            code_pattern = re.compile('&code=([\a-z]+)&')
            code: str = code_pattern.findall(raw_url)[0]
            return code

        except requests.exceptions.RequestException as e:
            self.logger.error(f'An error has occurred while making\
                the request: {e}')
            raise

        finally:
            webbrowser.quit()

    def get_credentials(self) -> None:
        '''
        Gets the credentials (access_token, refresh_token, and expires_at)
        received from the API making a POST request.
        Finally, these credentials are stored in an .env file
        using the set_key function.
        '''
        try:
            # Set the data required for the POST request
            data: Dict[str, Union[str, int]] = {
                    'client_id': self.client_id,
                    'client_secret': self.secret_key,
                    'code': self.get_oauth_code(),
                    'grant_type': 'authorization_code'
                    }

            response: Dict[str, Any] = requests.post(
                url=self.URL,
                data=data
            )

            if response.raise_for_status() != 200:
                raise requests.exceptions.HTTPError("HTTP error has occurred")

            response_credentials = response.json()

            access_token: str = response_credentials["access_token"]
            refresh_token: str = response_credentials["refresh_token"]
            expires_at: str = response_credentials["expires_at"]

            set_key('.env', 'ACCESS_TOKEN', access_token)
            set_key('.env', 'REFRESH_TOKEN', refresh_token)
            set_key('.env', 'EXPIRES_AT', str(expires_at))

        # If there are any exception, it will be stored in a log file
        except (
            requests.exceptions.RequestException,
            KeyError,
            json.JSONDecodeError
        ) as e:
            self.logger.error(f'An error has ocurred while\
                requesting credentials:\n {e}')
            raise

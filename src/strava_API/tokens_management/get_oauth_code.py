import re
import webbrowser

import requests
from requests import Request

from config import authorization_url, header_code_OAuth
from logger.logger import ErrorLogger

logger = ErrorLogger()


class GetOAuthCode:
    authorization_url: str
    header_code_OAuth: str

    def get_oauth_code(self) -> str:
        """
        Launches a web browser to retrieve the OAuth code from Strava.

        """

        try:
            get_url_code = Request(
                "GET", authorization_url, params=header_code_OAuth
            ).prepare()
            # Open the browser to get the URL with the code
            webbrowser.open(get_url_code.url)

            # Get the URL qith the code from the user
            print("Paste here the URL from the browser: ", end="")
            url_with_code = input().strip()

            # Extract the code from the URL using this regular expression
            code_pattern = re.compile("&code=([\a-z]+)&")
            code_match = code_pattern.search(url_with_code)

            if not code_match:
                logger.error("Could not retrieve OAuth code from URL")

            return code_match.group(1)

        except requests.RequestException as e:
            error_map = {
                requests.exceptions.HTTPError: "HTTP error",
                requests.exceptions.ConnectTimeout: "Timeout error",
                requests.exceptions.Timeout: "Timeout error",
                requests.exceptions.ConnectionError: "Connection error"
            }
            error = error_map.get(type(e), "Other kind of error")
            logger.error(f"Error: {e}. {error} occurred.")
            raise
        except Exception as e:
            logger.error(f"Other kind of error has occurred: {e}")

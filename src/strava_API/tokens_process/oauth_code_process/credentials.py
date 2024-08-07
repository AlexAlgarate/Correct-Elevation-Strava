from __future__ import annotations

from utils import config


class Credentials:
    """
    Initializes a instance of the Credentials class.

    Parameters:
        email (str): The email associated with the Strava account.
        password (str): The password associated with the Strava account.
    """

    email: str = config.EMAIL
    password: str = config.PASSWORD

    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password
        if self.email and self.password is None:
            raise ValueError("Credentials must be provided.")

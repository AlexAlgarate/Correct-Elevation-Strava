from __future__ import annotations

from utils.config import EMAIL, PASSWORD


class Credentials:
    """
    Initializes a instance of the Credentials class.

    Parameters:
        email (str): The email associated with the Strava account.
        password (str): The password associated with the Strava account.
    """

    email: str = EMAIL
    password: str = PASSWORD

    def __init__(self, email: str, password: str) -> None:
        if email is None or password is None:
            raise ValueError("Credentials must be provided.")
        self.email: str = email
        self.password: str = password

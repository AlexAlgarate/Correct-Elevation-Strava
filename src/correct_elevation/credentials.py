from __future__ import annotations


class Credentials:
    """
    Initializes a instance of the Credentials class.

    Parameters:
        email (str): The email associated with the Strava account.
        password (str): The password associated with the Strava account.
    """

    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password

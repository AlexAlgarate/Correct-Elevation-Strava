from __future__ import annotations


class Credentials:
    """
    Initializes a instance of the Credentials class.

    Parameters:
        email (str): The email associated with the Strava account.
        password (str): The password associated with the Strava account.
    """
    email: str
    password: str

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

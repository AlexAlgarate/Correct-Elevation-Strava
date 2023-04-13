from __future__ import annotations


class Credentials:
    email: str
    password: str

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

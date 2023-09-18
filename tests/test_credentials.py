import os
import sys
import unittest
import re

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import EMAIL, PASSWORD
from src.correct_elevation.credentials import Credentials


class TestCredentials(unittest.TestCase):
    email = EMAIL
    password = PASSWORD
    credentials = Credentials(email, password)

    def test_credentials_instance(self):

        self.assertIsInstance(self.credentials, Credentials)

    def test_valid_email_format(self):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        self.assertTrue(re.match(email_regex, self.email))
        self.assertFalse(re.match(email_regex, "1234_exampleexample.org"))

    def test_credentials_instance_with_empty_fields(self):
        email = ""
        password = ""
        self.assertNotEqual(email, self.credentials.email)
        self.assertNotEqual(password, self.credentials.password)


if __name__ == "__main__":
    unittest.main()

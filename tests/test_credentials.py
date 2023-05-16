from src.correct_elevation.credentials import Credentials


class TestCredentials:
    def test_credentials_instance(self):
        email = "is_an_example@is_an_example.com"
        password = "1234IsNotSecure"
        credentials = Credentials(email, password)
        assert isinstance(credentials, Credentials)
        assert credentials.email == email
        assert credentials.password == password

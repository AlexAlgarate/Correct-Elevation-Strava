import time
import unittest

from assertpy import assert_that

from config import ACCESS_TOKEN, EXPIRES_AT, REFRESH_TOKEN
from src.strava_api.tokens_process.generate_credentials import GenerateAccessToken
from src.strava_api.tokens_process.oauth_code_process.get_oauth_code import (
    GetOauthCode,
)
from src.strava_api.tokens_process.refresh_token import RefreshTokenManager

refresh = RefreshTokenManager
generate_credentials = GenerateAccessToken()


class TestSummary(unittest.TestCase):
    def test_code_oauth_is_str(self):
        """
        Test if the OAuth code is a string

        Returns:
            - str
        """
        code = GetOauthCode()
        assert_that(code.get_oauth_code()).is_type_of(str)

    def test_generate_credentials(self):
        """
        Create an instance of the class to generate the credentials and check
        if the access token, refresh_token and expires_at are created, they are
        not None and are strings.
        ACCESS_TOKEN, REFRESH_TOKEN and EXPIRES_AT are imported from the
        config module, that uses os.getenv() method to access to these
        environment variables.
        """
        generate_credentials.generate_access_token()

        assert_that(ACCESS_TOKEN).is_not_none().is_type_of(str)
        assert_that(REFRESH_TOKEN).is_not_none().is_type_of(str)
        assert_that(EXPIRES_AT).is_not_none().is_type_of(str)

    def test_expires_at_is_an_integer(self):
        """
        Test if EXPIRES_AT is an integer. If not True, it cannot be used
        in the check_expired() method of the RefresehTokenManager class.

        Returns:
            - str
        """
        assert_that(EXPIRES_AT).is_instance_of(str)

    def test_check_expired_returns_bool(self):
        """
        Test that check_expired() method returns bool.

        Returns:
            - bool
        """
        assert_that(refresh._check_expired(self)).is_instance_of(bool)

    def test_check_expired(self):
        """
        Test potencial results of the check_expired() method.

        Returns:
            - True if Expires_at is lower than current time
            - False otherwise
        """
        current_time = int(time.time())
        expired_time = str(current_time - 3600)
        if expired_time < str(current_time):
            assert_that(refresh._check_expired(self)).is_true()
        else:
            assert_that(refresh._check_expired(self)).is_false()

    def test_expired_returns_false_when_expires_at_is_none(self):
        """
        test_expired_returns_false_when_expires_at_is_none _summary_
        """
        expires_at_is_none = refresh.EXPIRES_AT = None
        if expires_at_is_none:
            assert_that(refresh._check_expired(self)).is_false()


if __name__ == "__main__":
    unittest.main()


#########################
# **** TODO ****
#########################
# def test_get_activities():
#     # Test that _get_activities returns a non-empty list
#     activities = summary._get_activities(1)
#     assert isinstance(activities, list)
#     assert len(activities) > 0


# def test_get_all_activities():
#     # Test that _get_all_activities returns a non-empty list
#     activities = summary._get_all_activities()
#     assert isinstance(activities, list)
#     assert len(activities) > 0


# def test_normalize_activities():
#     # Test that normalize_activities returns a pandas DataFrame
#     activities = summary._get_all_activities()
#     df = summary.normalize_activities(activities)
#     assert isinstance(df, pd.DataFrame)


# def test_fetch_summary_data():
#     # Test that fetch_summary_data returns a pandas DataFrame
#     df = summary.fetch_summary_data()
#     assert isinstance(df, pd.DataFrame)

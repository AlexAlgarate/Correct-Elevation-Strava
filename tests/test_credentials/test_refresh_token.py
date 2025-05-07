from unittest.mock import patch

import pytest
from pytest import fixture

from src.strava_API.tokens_process.refresh_token import RefreshTokenManager


@fixture
def refresh():
    return RefreshTokenManager()


class TestCheckAccessTokenExpired:
    def test_expiration_is_smaller_current_time(self, refresh: RefreshTokenManager):
        refresh.current_time = 1234
        with patch("src.strava_api.tokens_process.refresh_token.EXPIRES_AT", 123):
            assert refresh._check_expired() is True

    def test_expiration_is_greater_current_time(self, refresh: RefreshTokenManager):
        refresh.current_time = 123
        with patch("src.strava_api.tokens_process.refresh_token.EXPIRES_AT", 1234):
            assert refresh._check_expired() is False

    def test_expiration_is_equals_current_time(self, refresh: RefreshTokenManager):
        refresh.current_time = 123
        with patch("src.strava_api.tokens_process.refresh_token.EXPIRES_AT", 123):
            assert refresh._check_expired() is False

    def test_check_expired_value_error(self, refresh: RefreshTokenManager):
        with patch(
            "src.strava_api.tokens_process.refresh_token.EXPIRES_AT",
            "invalid_timestamp",
        ):
            with pytest.raises(ValueError) as exception:
                refresh._check_expired()
            assert "EXPIRES_AT value is not a valid integer timestamp" in str(
                exception.value
            )

    def test_check_expired_type_error(self, refresh: RefreshTokenManager):
        refresh.current_time = "123"
        with patch("src.strava_api.tokens_process.refresh_token.EXPIRES_AT", 123):
            with pytest.raises(TypeError) as exception:
                refresh._check_expired()
            assert "EXPIRES_AT has to be an integer, not a string" in str(
                exception.value
            )

    def test_check_expired_is_boolean(self, refresh: RefreshTokenManager):
        refresh.current_time = 123
        with patch("src.strava_api.tokens_process.refresh_token.EXPIRES_AT", 123):
            assert isinstance(refresh._check_expired(), bool)

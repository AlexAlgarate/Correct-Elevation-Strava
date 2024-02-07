import pytest
from selenium.webdriver.chrome.webdriver import WebDriver

from src.correct_elevation.strava_activity import StravaActivity


@pytest.fixture
def strava_activity_instance(driver: WebDriver):
    return StravaActivity(driver, activity_id=123)


def test_get_activity_url(strava_activity_instance: StravaActivity):
    url = strava_activity_instance._get_activity_url()
    assert url == "https://www.strava.com/activities/123"

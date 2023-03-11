import pandas as pd
from utils.summary import Summary

# Initialize a Summary object for use in tests
summary = Summary()


def test_get_activities():
    # Test that _get_activities returns a non-empty list
    activities = summary._get_activities(1)
    assert isinstance(activities, list)
    assert len(activities) > 0


def test_get_all_activities():
    # Test that _get_all_activities returns a non-empty list
    activities = summary._get_all_activities()
    assert isinstance(activities, list)
    assert len(activities) > 0


def test_normalize_activities():
    # Test that normalize_activities returns a pandas DataFrame
    activities = summary._get_all_activities()
    df = summary.normalize_activities(activities)
    assert isinstance(df, pd.DataFrame)


def test_fetch_summary_data():
    # Test that fetch_summary_data returns a pandas DataFrame
    df = summary.fetch_summary_data()
    assert isinstance(df, pd.DataFrame)

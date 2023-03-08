# Correct-Elevation-Strava

This script is designed to correct elevation data for Strava activities that have an elevation gain of 0. It uses Selenium to log into Strava and correct the elevation data for each activity in a specified database.

## Requirements

* Python 3.6 or higher
* Chrome web browser
* ChromeDriver (make sure to match the version with your Chrome browser)
* The following Python packages: decouple, dotenv, sqlalchemy, selenium, webdriver_manager

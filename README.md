# Correct-Elevation-Strava

This script is designed to correct elevation data for Strava activities that have an elevation gain of 0. It uses Selenium to log into Strava and correct the elevation data for each activity in a specified database.
 
## Requirements

* Python 3.6 or higher
* Chrome web browser
* ChromeDriver ([make sure to match the version with your Chrome browser](chrome://settings/help))
* The following Python packages: decouple, dotenv, sqlalchemy, selenium, webdriver_manager

## Setup

* Clone this repository or download the script.
* Install the required Python packages: pip install -r requirements.txt
* Download and install ChromeDriver.
* Create a .env file in the same directory as the script and set the following variables:

```
EMAIL=your_strava_email
PASSWORD=your_strava_password
ENGINE=your_sqlalchemy_engine
```
* EMAIL: your Strava email address
* PASSWORD: your Strava password
* ENGINE: your SQLAlchemy engine string, e.g. postgresql://user:password@localhost/mydatabase

## Usage

1. Open a terminal or command prompt and navigate to the directory where the script is located.
2. Run the script python ***strava_elevation_correction.py***

The script will log into Strava, retrieve a list of activity IDs from the specified database, and correct the elevation data for each activity with an elevation gain of 0.

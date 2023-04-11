# Correct-Elevation-Strava

![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Flake8](https://img.shields.io/badge/code%20style-flake8-blue)

This script is designed to correct elevation data for Strava activities that have an elevation gain of 0. It uses Selenium to log into Strava and correct the elevation data for each activity in a specified database.
To do this, it first uses the Strava API to get a summary of all sports activities. Then, using filters using the Pandas library, the ids of the activities whose elevation gain was 0 meters are obtained. The list of these ids is used in the Selenium script to correct the elevation.

## Requirements

* Python 3.6 or higher
* Chrome web browser
* The Chrome version (Settings->Help->Chrome's information)
(* Download [ChromeDriver](https://chromedriver.chromium.org/))
* Install the dependencies from the requirements.txt file

## Setup

* Clone this repository or download the script.
* Install the required Python packages:

```text
pip install -r requirements.txt
```

* Create the App/API Connection in Srava ([follow step by step this tutorial](https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86))
* Create a .env file in the same directory as the script and set the following variables:

```text
EMAIL=your_strava_email
PASSWORD=your_strava_password
ENGINE=your_sqlalchemy_engine
STRAVA_ID=your Strava ID
STRAVA_SECRET_KEY=your Strava secret key
```

* EMAIL: your Strava email address to log in
* PASSWORD: your Strava password to log in
* ENGINE: your SQLAlchemy engine string, e.g. postgresql://user:password@localhost/mydatabase
* STRAVA_ID: get from "My API Aplication" in Strava->Settings
* STRAVA_SECRET_KEY: get from "My API Aplication" in Strava->Settings

## Usage

1. Open a terminal or command prompt and navigate to the directory where the script is located.
2. Run the Python file ***main.py***

```text
*main.py*
```

To summarize, the script will retrieve the access token from the Strava API, obtain a global summary of Strava activities and using Pandas, it filters activities with a total elevation of 0 meters, finally it retrieves their IDs. Then, using Selenium, it will log into Strava and retrieve the list of activity IDs to access each activity's page (www.strava.com/activities/8861948081, where 8861948081 is one of the IDs with zero elevation), and search for the "Correct Elevation" button. It will click on it and move to the next activity on the list.

## Contributing

If you'd like to contribute to Correct-Elevation-Strava, please fork the repository and create a pull request with your changes. We welcome all contributions!

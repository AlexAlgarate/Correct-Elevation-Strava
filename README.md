# Correct elevation from Strava activities 

## Overview
This project addresses the issue of the malfunctioning barometric sensor in Garmin Fenix devices, causing inaccurate elevation data to be displayed (*[it's a widespread issue in the Garmin Fenix 3 range](https://forums.garmin.com/outdoor-recreation/outdoor-recreation-archive/f/fenix-5-series/168518/fenix-3-hr---temperature-and-baromerter-not-working)*). By leveraging Strava's correction feature for elevation data, the project aims to provide a solution to this problem (*[as you can see in this example, many people have the same issue as me with older activities](https://communityhub.strava.com/t5/strava-features-chat/elevation-correction/td-p/23187#:~:text=If%20you%20record%20with%20one,our%20database%20of%20barometric%20data.)*).

## How it Works *[(Strava Documentation)](https://support.strava.com/hc/en-us/articles/216919447-Elevation-for-Your-Activity)*
Strava's elevation correction process involves cross-referencing GPS data with their database of barometric data to ensure accurate elevation readings. Elevation data on Strava is smoothed and thresholds are set to maintain accuracy, particularly for activities recorded on devices without a barometric altimeter.

## Functionality
The program automates the process of correcting elevation data on Strava for activities recorded with Garmin Fenix devices experiencing barometric sensor issues. It follows a set of steps outlined below:

**1.** Create a Strava API using *[the provided guide](https://developers.strava.com/docs/getting-started/)*.

<a>
    <img
  alt="Image of Strava webpage where you can create the API" src="/images/strava_api_example.png" style="box-shadow: 5px 5px 5px grey; width:75%; height:75%; border:2px"
    />
</a>

<br>

**2.** Fill in the required credentials (CLIENT_ID, SECRET_KEY, USER, PASSWORD) in a .env file.

<a>
    <img
  alt="Image of the .env file with the name of variables and theis example values" src="/images/env.png" style="box-shadow: 5px 5px 5px grey; width:75%; height:75%; border:2px"
    />
</a>

<br>

**3.** Setup virtual environment

- Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Windows:

```python
python -m venv .venv
.venv\Scripts\activate
```

**4.** Install the project dependencies using PIP


```python
pip install -r .\requirements.txt
```

The following steps are automated when running the program:


```python
python ./main.py
```

**1.** Obtain an access token to make API requests to Strava.  
**2.** Fetch activity IDs for running and cycling activities with 0 meters of elevation gain.  
**3.** Utilize Selenium to automate the elevation correction process on Strava by logging in, navigating to the activity URLs, and initiating the correction process.

Additionally, it's worth mentioning that the program automatically handles token management. The access token, refresh token and expiration date are stored in the `.env` file. Upon subsequent use, the program will automatically retrieve the token, check for expiration, and generate a new one if necessary.

## Example

- Example of some running activities with elevation (corrected by Strava) and others with 0 meters of elevation that need to be corrected with the program  

<a>
    <img
  alt="Image of Strava webpage displaying some sport activities" src="/images/activities.png" style="box-shadow: 5px 5px 5px grey; width:75%; height:75%; border:2px"
    />
</a>

<br>

- Example of an activity recorded by Garmin Fenix with 0 meters of elevation gain, requiring correction using Strava options.

<a>
    <img
  alt="Image of Strava webpage of one running activity with 0 meters of elevation gain" src="/images/preview_0m.png" style="box-shadow: 5px 5px 5px grey; width:75%; height:75%; border:2px"
    />
</a>

<br>

- This is the menu options of each activity where various parameters can be edited, including the one we need, 'correct elevation'. 

<a>
    <img
  alt="Image of the menu options of the running activity" src="/images/options_correct_elevation.png" style="box-shadow: 5px 5px 5px grey; width:30%; height:30%; border:2px"
    />
</a>

<br>

- When we click on the 'correct elevation' button, a popup window appears where we confirm the operation.

<a>
    <img
  alt="Image of the popup window where you can confirm the proccess" src="/images/click_correct.png" style="box-shadow: 5px 5px 5px grey; width:100%; height:100%; border:2px"
    />
</a>

<br>

- And this is the final result, an activity whose elevation has been corrected using Strava's databases.

<a>
    <img
  alt="Image of Strava webpage where the activity has been corrected" src="/images/activity_corrected.png" style="box-shadow: 5px 5px 5px grey; width:100%; height:100%; border:2px"
    />
</a>

<br>

## Conclusion
By automating the elevation correction process on Strava, users can ensure accurate elevation data for their activities, mitigating the impact of barometric sensor issues in Garmin Fenix devices. The project provides a practical solution for maintaining the integrity of elevation data in fitness tracking and analysis.


# TODO

- [ ] Test activity fetcher
- [ ] Test filter activities
- [x] Test credentials
- [x] Test extract code
- [x] Test request credentials
- [ ] Test get access token
- [x] Test refresh token
- [ ] Test summary
- [ ] Test strava activities
- [x] Test login strava
- [x] Test get oauth code
- [ ] Test get latest activities

[ ] CI/CD Github Actions (launch Chrome browser) to correct elevation and running tests.

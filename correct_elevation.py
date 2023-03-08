import os

from get_ids_database import get_ids_from_database

from dotenv import load_dotenv
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
ENGINE = create_engine(os.getenv('ENGINE'))
SECS = 10
QUERY = '''
    SELECT id
    FROM "Summary_Strava"
    WHERE sport_type = \'Run\' and
    total_elevation_gain = \'0\' and
    month = \'9\' and
    year = \'2022\';
'''
ID_LIST = get_ids_from_database(QUERY, ENGINE)


def main():

    # Set options
    options = Options()
    options.add_argument('--start-maximized')
    options.add_experimental_option("detach", True)

    # Start the driver
    with webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    ) as driver:
        # Load the login page
        driver.get('https://www.strava.com/login')

        # Fill in the email and password fields
        email_field = WebDriverWait(driver, SECS).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
        )
        email_field.send_keys(EMAIL)
        password_field = WebDriverWait(driver, SECS).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        password_field.send_keys(PASSWORD)

        # Click on the login button
        login_button = driver.find_element(By.XPATH, '//*[@id="login-button"]')
        login_button.click()

        # Loop through the activity IDs
        for activity_id in ID_LIST:
            # Load the activity page
            activity_url = f'https://www.strava.com/activities/{activity_id}'
            driver.get(activity_url)

            # Click on the options button
            options_button = WebDriverWait(driver, SECS).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/nav/div/button/div'))
            )
            options_button.click()

            # Click on the correct elevation option
            correct_elevation_option = WebDriverWait(driver, SECS).until(
                EC.presence_of_element_located((By.XPATH, '(//*[@id="react-list-item"]/div/a)[2]'))
            )
            correct_elevation_option.click()

            # Click on the button to correct the activity
            correct_activity_button = WebDriverWait(driver, SECS).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button'))
            )
            correct_activity_button.click()

        # Wait for a few seconds before closing the driver
        driver.implicitly_wait(15)


if __name__ == '__main__':
    main()

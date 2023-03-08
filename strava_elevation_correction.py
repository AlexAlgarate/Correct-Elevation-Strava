from decouple import config
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

EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
ENGINE = create_engine(config('ENGINE'))
SECS = 10


def get_activity_url(activity_id):
    return f'https://www.strava.com/activities/{activity_id}'


def login(driver) -> None:
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


def correct_elevation(driver) -> None:
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


def main():
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
        login(driver)
        query = (
            'SELECT id '
            'FROM "Summary_Strava" '
            'WHERE sport_type = \'Run\' and '
            'total_elevation_gain = \'0\' and '
            'year > \'2018\';'
        )
        id_list = get_ids_from_database(query, ENGINE)
        for activity_id in id_list:
            activity_url = get_activity_url(activity_id)
            driver.get(activity_url)
            correct_elevation(driver)
        driver.implicitly_wait(15)


if __name__ == '__main__':
    main()

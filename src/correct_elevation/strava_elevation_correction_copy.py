from decouple import config

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time


load_dotenv()

EMAIL = config("STRAVA_EMAIL")
PASSWORD = config("STRAVA_PASSWORD")
# ENGINE = create_engine(config('ENGINE'))
SECS = 10


def get_activity_url(activity_id) -> str:
    """
    Returns the URL of the Strava activity given an activity ID.
    """
    return f"https://www.strava.com/activities/{activity_id}"


def login(driver) -> None:
    """
    Logs into Strava using the given Selenium webdriver.

    """
    driver.get("https://www.strava.com/login")

    # Fill in the email and password fields
    email_field = WebDriverWait(driver, SECS).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_field.send_keys(EMAIL)

    password_field = WebDriverWait(driver, SECS).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.send_keys(PASSWORD)

    # Click on the login button
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()


def correct_elevation(driver) -> None:
    """
    Corrects the elevation data of a Strava activity
    using the given Selenium webdriver.

    """
    # Click on the options button
    try:
        options_button = WebDriverWait(driver, SECS).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.slide-menu.drop-down-menu.enabled.align-top")
            )
        )
        options_button.click()
        time.sleep(3)
        print("\nHA PULSADO EL BOTÓN DE OPCIONES, TEN, UN TRIPI\n")
    except Exception:
        print("NO ENCUENTRA LA CLASS NI A M.D.C.")
    # Click on the correct elevation option
    try:
        # options_menu = WebDriverWait(driver, SECS).until(
        #     EC.presence_of_all_elements_located((
        #         By.ID, 'react-list-item'))
        # )
        correct_elevation_button = WebDriverWait(driver, SECS).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.options.open-menu"))
        )
        print("\n\nEL BOTÓN\n\n")
        print(correct_elevation_button)
        # for value, element in enumerate(options_menu):
        #     # print(str(value) + "CLASS: " + str(element))
        #     print("AHORA EL SEGUNDO ELEMENTO")
        #     print(type(element))
        #     print(str(value) + str(element))
        print("\n\nEL BOTÓN\n\n")

        print("\n########\n##########\n###########\n")
        for value, element in enumerate(correct_elevation_button):
            # print(str(value) + "CLASS: " + str(element))
            # print(f"EL BOTÓN Y SU ELEMENTO: {element[value]}")
            # print(type(element))
            print(str(value) + str(element))
    except Exception as e:
        print("NO LO ENCUENTRA JODEEEEEEEEERRRRRRRRRRR", e)
    # correct_elevation_option.click()
    # print("HA PULSADO EN CORREGIR")
    # # Click on the button to correct the activity
    # correct_activity_button = WebDriverWait(driver, SECS).until(
    #     EC.presence_of_element_located((
    #         By.XPATH, '/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button'))
    # )
    # correct_activity_button.click()
    # print("HA PULSADO EL BOTÓN Y LA ACTIVIDAD ESTÁ CORREGIDA")


def main() -> None:
    # Set the options that you need
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    # Start the driver
    with webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    ) as driver:
        # Run the log in process
        login(driver)

        # Get the list of activities from the query
        id_list = [8040982449]
        # id_list = [435158118, 563961044]

        # Correct the elevation to the activities
        for activity_id in id_list:
            activity_url = get_activity_url(activity_id)
            driver.get(activity_url)
            correct_elevation(driver)
        driver.implicitly_wait(15)


if __name__ == "__main__":
    main()

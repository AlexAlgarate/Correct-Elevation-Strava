import time

from decouple import config
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

load_dotenv()

EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
SECS = 10

# Put you Chromedriver path
driver_path = 'C:\\Users\\alexa\\Downloads\\chromedriver_win32\\chromedriver.exe'

s = webdriver.Chrome(executable_path=driver_path)
s.get('https://www.strava.com/login')
action = ActionChains(s)
s.maximize_window()

user = s.find_element(By.XPATH, '//*[@id="email"]').send_keys(f'{EMAIL}')
psw = s.find_element(By.XPATH, '//*[@id="password"]').send_keys(f'{PASSWORD}')
log_in = s.find_element(By.XPATH, '//*[@id="login-button"]')
log_in.click()
time.sleep(SECS)
expand_training = s.find_element(By.XPATH, '//*[@id="container-nav"]/ul[1]/li[2]/a')
action.move_to_element(expand_training).perform()
time.sleep(SECS)
my_activities = s.find_element(By.XPATH, '//*[@id="container-nav"]/ul[1]/li[2]/ul/li[2]/a')
my_activities.click()
time.sleep(SECS)
activity = s.find_element(By.XPATH, '//*[@id="search-results"]/tbody/tr[2]/td[3]/a')
activity.click()
time.sleep(SECS)
options = s.find_element(By.XPATH, '/html/body/div[1]/div[3]/nav/div/button/div')
options.click()
time.sleep(SECS)
correct_elevation = s.find_element(By.XPATH, '(//*[@id="react-list-item"]/div/a)[2]')
correct_elevation.click()
activity_corrected = s.find_element(By.XPATH, '/html/body/reach-portal/div[2]/div/div/div/form/div[2]/button')
activity_corrected.click()

time.sleep(15)
s.close()

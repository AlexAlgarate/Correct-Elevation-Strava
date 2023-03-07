from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
# chrome_options = Options()
options.add_experimental_option("detach", True)
driver_path = 'C:\\Users\\alexa\\Downloads\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(driver_path, options=options)


driver.get('https://eltiempo.es')

# Abre el navegador y acepta las cookies
# WebDriverWait(driver, 5)\
#     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
#                                       'button.didomi-components-button didomi-button didomi-dismiss-button didomi-components-button--color didomi-button-highlight highlight-button'.replace(" ", "."))))\
#     .click()  

# # Busca Madrid
# WebDriverWait(driver, 5)\
#     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
#                                       'input#term')))\
#     .send_keys('Huelva')

# # Click en buscar
# WebDriverWait(driver, 5)\
#     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
#                                       'i.icon icon-sm icon-search'.replace(" ", "."))))\
#     .click()

# # Click en la ciudad de Madrid
# WebDriverWait(driver, 5)\
#     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
#                                       'i.icon_weather_s icon icon-sm icon-city'.replace(" ", "."))))\
#     .click()




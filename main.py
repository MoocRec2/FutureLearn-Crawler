import time
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import json
from json import JSONDecodeError
from db_connector import Thread
from pprint import pprint

driver = webdriver.Chrome('C:/chromedriver')


def check_page_load(by, delay, element_id):
    count = 0
    while count < 10:
        try:
            my_elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, element_id)))
            # print(element_id, "Page is ready!")
            break
        except TimeoutException:
            # print(element_id, 'Page is not yet ready, checking again...')
            pass
        count += 1


driver.get('https://www.futurelearn.com/sign-in')

email_input_element = driver.find_element_by_id('email')
password_input_element = driver.find_element_by_id('password')

email_input_element.send_keys('smrbasil4@gmail.com')
password_input_element.send_keys('nvidia1024')

sign_in_btn = driver.find_element_by_name('button')
sign_in_btn.click()

check_page_load(By.CLASS_NAME, 1, 'a-heading')



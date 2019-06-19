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

courses_grid = driver.find_element_by_class_name('m-grid-of-cards')

courses_elements = driver.find_elements_by_class_name('m-card')

def get_threads():
    activity_feed = driver.find_element_by_class_name('m-feed')
    feed_items = driver.find_elements_by_class_name('m-feed-item__body')

for course_element in courses_elements:
    course_element.click()
    check_page_load(By.CLASS_NAME, 1, 'm-run-nav__container')
    nav_bar = driver.find_element_by_class_name('m-run-nav')
    nav_bar_elements = nav_bar.find_elements_by_class_name('m-run-nav__item')
    activity_element = nav_bar_elements[1]
    activity_element.click()

    check_page_load(By.CLASS_NAME, 1, 'm-feed')


    break

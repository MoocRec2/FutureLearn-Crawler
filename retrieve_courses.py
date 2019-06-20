import time
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import json
from json import JSONDecodeError
from db_connector import Thread
from pprint import pprint
from selenium.webdriver.chrome.options import Options
import requests

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome('C:/chromedriver', options=options)

print('Beginning Retrieving Courses')


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


print('Authenticating')
driver.get('https://www.futurelearn.com/sign-in')

email_input_element = driver.find_element_by_id('email')
password_input_element = driver.find_element_by_id('password')

email_input_element.send_keys('smrbasil4@gmail.com')
password_input_element.send_keys('nvidia1024')

sign_in_btn = driver.find_element_by_name('button')
driver.execute_script('window.scroll(0, 500)')
sign_in_btn.click()

# Check whether the browser is in the 'Your Courses' Page
check_page_load(By.CLASS_NAME, 1, 'a-heading')
print('Successfully Authenticated')

courses_grid = driver.find_element_by_class_name('m-grid-of-cards')

courses_elements = driver.find_elements_by_class_name('m-card')

print('Total No. of Added Courses: ', courses_elements.__len__())

cookies = driver.get_cookies()
cookies_dict = {}
for cookie in cookies:
    cookies_dict[cookie.get('name')] = cookie.get('value')
print(cookies)

r = requests.get('https://www.futurelearn.com/your-courses?all_courses=true&filter_name=in-progress',
                 cookies=cookies_dict)
response = r.text
print(response)

driver.quit()

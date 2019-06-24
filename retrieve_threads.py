import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import json
from json import JSONDecodeError
from db_connector import Thread
from db_connector import Course
from db_connector import FutureLearnThreads
from pprint import pprint
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome('C:/chromedriver', options=options)

print('Beginning Authentication')


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
driver.execute_script('window.scroll(0, 500)')
sign_in_btn.click()

# Check whether the browser is in the 'Your Courses' Page
check_page_load(By.CLASS_NAME, 1, 'a-heading')
print('Authenticated')

# Retrieve courses from the database
courses = Course.get_all_future_learn_courses()

count = 0
for x in courses:
    count += 1
print('Retrieved Courses from the Database (Count = {})'.format(count))

# For every course item in the user's profile
base_url = 'https://www.futurelearn.com'
for course_record in courses:
    driver.get(base_url + course_record['path'])

    # check_page_load(By.CLASS_NAME, 1, 'm-run-nav__container')

    nav_bar = driver.find_element_by_class_name('m-run-nav')
    nav_bar_elements = nav_bar.find_elements_by_class_name('m-run-nav__item')
    activity_element = nav_bar_elements[1]
    activity_element.click()

    # Check whether the ACTIVITY page has loaded
    check_page_load(By.CLASS_NAME, 1, 'm-feed')

    activity_feed = driver.find_element_by_class_name('m-feed')
    feed_items = activity_feed.find_elements_by_class_name('m-feed-item__body')

    print('Extracting Thread Information')
    threads = []
    for feed_item in feed_items:
        heading = feed_item.find_element_by_class_name('m-feed-item__context-heading')
        item_link_tag = heading.find_element_by_tag_name('a')
        link = item_link_tag.get_attribute('href')
        title = item_link_tag.text

        link_components = link.split('/')
        thread_id = link_components[link_components.__len__() - 1]

        thread_details = {'id': thread_id, 'course_key': course_record['key'], 'title': title, 'link': link}
        threads.append(thread_details)

    print('Basic Information of ', threads.__len__(), ' threads have been extracted')
    print('Saving to Database')
    FutureLearnThreads.upsert_threads(threads)
    print('Basic Information has been saved to the database')

driver.quit()

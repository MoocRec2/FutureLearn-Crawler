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
from pprint import pprint
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('log-level=3')

driver = webdriver.Chrome('C:/chromedriver', options=options)


# print('Beginning Retrieving Thread Information')


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

# email_input_element = driver.find_element_by_id('email')
email_input_element = driver.find_element_by_name('email')
password_input_element = driver.find_element_by_name('password')

# email_input_element.send_keys('smrbasil4@gmail.com')
email_input_element.send_keys('smrbasil4@hotmail.com')
password_input_element.send_keys('nvidia1024')

# sign_in_btn = driver.find_element_by_name('button')
sign_in_btn = driver.find_element_by_class_name('button-wrapper_28yrv')
driver.execute_script('window.scroll(0, 500)')
sign_in_btn.click()

# Check whether the browser is in the 'Your Courses' Page
check_page_load(By.CLASS_NAME, 1, 'a-heading')
print('Successfully Authenticated')

courses_grid = driver.find_element_by_class_name('m-grid-of-cards')

courses_elements = driver.find_elements_by_class_name('m-card')

print('No. of Added Courses: ', courses_elements.__len__())

# For every course item in the user's profile
count = 0

for x in range(courses_elements.__len__()):
    courses_grid = driver.find_element_by_class_name('m-grid-of-cards')

    courses_elements = driver.find_elements_by_class_name('m-card')

    course_element = courses_elements[x]
    count += 1
    print('Course No.', count)
    course_link = course_element.find_element_by_tag_name('a')
    print('Course Link:', course_link.get_attribute('href'))
    course_link.click()

    check_page_load(By.CLASS_NAME, 1, 'm-run-nav__container')

    nav_bar = driver.find_element_by_class_name('m-run-nav')
    nav_bar_elements = nav_bar.find_elements_by_class_name('m-run-nav__item')
    activity_element = nav_bar_elements[1]
    activity_element.click()

    # Check whether the ACTIVITY page has loaded
    check_page_load(By.CLASS_NAME, 1, 'm-feed')

    activity_feed = driver.find_element_by_class_name('m-feed')
    feed_items = activity_feed.find_elements_by_class_name('m-feed-item__body')

    threads = []
    for feed_item in feed_items:
        heading = feed_item.find_element_by_class_name('m-feed-item__context-heading')
        item_link_tag = heading.find_element_by_tag_name('a')
        link = item_link_tag.get_attribute('href')
        title = item_link_tag.text

        thread_details = {'title': title, 'link': link}
        threads.append(thread_details)

    print('Information of ', threads.__len__(), ' threads have been extracted')

    # TODO: Navigate back to the YOUR COURSES page
    driver.get('https://www.futurelearn.com/your-courses')
    # pprint(threads)
    # break

driver.quit()

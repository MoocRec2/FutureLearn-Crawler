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

print('Retrieved Courses from the Database (Count = {})'.format(courses.count()))

course_count = 1
for course in courses:
    course_key = course['key']

    threads = FutureLearnThreads.get_threads_by_course(course_key)
    print('Retrieved {} Threads'.format(threads.count()))

    thread_count = 1
    for thread in threads:
        print('Analyzing Thread No.:', thread_count)
        driver.get(thread['link'])

        feed_element = driver.find_element_by_class_name('m-feed')
        # feed_element.get_attribute()
        comment_elements = feed_element.find_elements_by_tag_name('li')
        posts = []
        for comment_element in comment_elements:
            try:
                comment_id = comment_element.get_attribute('id')
                comment_body_div = comment_element.find_element_by_class_name('m-feed-item__body')

                content_div = comment_body_div.find_element_by_class_name('m-feed-item__content')
                reply_text = content_div.find_element_by_tag_name('p').text

                formatted_id = int(comment_id.split('_')[1])
                # print('comment_id  =', comment_id)
                # print('Reply Text =', reply_text)
                post_info = {'id': formatted_id, 'text': reply_text}
                posts.append(post_info)
            except:
                print('Exception Thrown, Proceeding to next')
        thread['posts'] = posts
        FutureLearnThreads.upsert_threads([thread])
        print('Updated Thread =', thread['id'])
        thread_count += 1

    break

driver.quit()

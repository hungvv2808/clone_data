import os
import time
from argparse import Namespace
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

timeout = 10


def url_process(func):
    def wrapper(**data):
        requires = ['url']
        for require in requires:
            if require not in data:
                return False
        u = urlparse(data['url'])
        data['url'] = os.path.join(f'{u.scheme}://', u.netloc, 'admin')
        return func(**data)
    return wrapper


@url_process
def get_cookies(**data):
    browser = webdriver.Chrome()
    browser.get(data['url'])
    try:
        # insert email
        WebDriverWait(browser, timeout).until(ec.presence_of_element_located((By.CLASS_NAME, 'ui-button--primary')))
        email_field = browser.find_element_by_id('account_email')
        email_field.send_keys(data['email'])
        next_btn = browser.find_element_by_class_name('ui-button--primary')
        next_btn.click()
        time.sleep(5)
        # insert pwd
        WebDriverWait(browser, timeout).until(ec.presence_of_element_located((By.CLASS_NAME, 'ui-button--primary')))
        account_password = browser.find_element_by_id('account_password')
        account_password.send_keys(data['password'])
        login_btn = browser.find_element_by_class_name('ui-button--primary')
        login_btn.click()
        print("Logged in -> Next step: Get data!")
    except Exception as e:
        print("Exception: " + str(e))
    cookies = browser.get_cookies()
    browser.quit()
    return cookies


@url_process
def get_data(**data):
    n = Namespace(**data)
    if 'since_id' in n:
        entity = f'{n.entity}.json?since_id={n.since_id}'
    else:
        entity = f'{n.entity}.json'
    real_url = os.path.join(n.url, 'api', n.api_version, entity)

    session = requests.Session()
    for cookie in n.cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    response = session.get(real_url)
    if response.status_code != 200:
        print('Error: ' + str(response.status_code))
        return
    return response.text

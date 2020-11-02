'''
셀레니움 엘리먼트 검색 방식들 탐색
https://www.selenium.dev/documentation/ko/getting_started_with_webdriver/locating_elements/

- id
- css_selector
- class_name
- xpath
'''

from selenium import webdriver
from time import sleep

URL = 'https://github.com/'
xpath = '/html/body/div[4]/main/div[1]/div[1]/div/div/div[2]/div[1]/form/button'

browser = webdriver.Chrome()
browser.get(URL)
sleep(3)
browser.find_element_by_xpath(xpath).click()
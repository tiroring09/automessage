'''
selenium file upload 방식
'''

from selenium import webdriver

URL = 'file:///C:/Users/multicampus/Documents/SANDBOX/barcode_reader/index.html'
FILE = 'C:/Users/multicampus/Documents/SANDBOX/barcode_reader/find_element.png'

browser = webdriver.Chrome()
browser.get(URL)

browser.find_element_by_tag_name('input').send_keys(FILE)
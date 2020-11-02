from selenium import webdriver
from time import sleep

#####################CONSTANTS###########################
URL = 'https://www.naver.com'

#####################CONSTANTS###########################END

browser = webdriver.Chrome()
browser.get(URL)
sleep(3)

browser.refresh()
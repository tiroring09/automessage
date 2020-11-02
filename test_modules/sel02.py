'''
config 불러와서 로그인하기
'''
from selenium import webdriver
from decouple import config
from time import sleep

#####################CONSTANTS###########################
loginURL = 'https://seller.shopee.sg/account/signin'
searchURL = 'https://seller.shopee.sg/portal/sale?search='
ID = config('SHOPEE_ID')
PW = config('SHOPEE_PW')
test_key = '201003ABB5626D'
order_id = test_key
#####################CONSTANTS###########################END

browser = webdriver.Chrome()
browser.get(loginURL)
sleep(1)

# 로그인
form_elements = browser.find_elements_by_css_selector('input')
ID_form = form_elements[0]
PW_form = form_elements[1]

ID_form.send_keys(ID)
PW_form.send_keys(PW)

button = browser.find_element_by_css_selector('button')
button.click()
sleep(1)

# order id 검색
browser.get(searchURL + order_id)
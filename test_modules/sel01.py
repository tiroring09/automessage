'''
셀레니움 설치 및 최초 실행
'''
from selenium import webdriver

#####################CONSTANTS###########################
loginURL = 'https://seller.shopee.sg/account/signin'
searchURL = 'https://seller.shopee.sg/portal/sale?search={키워드}'

#####################CONSTANTS###########################END

browser = webdriver.Chrome()
browser.get(loginURL)
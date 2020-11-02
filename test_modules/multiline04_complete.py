'''
multiline 모듈화
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


### CONSTANTS ###
url = 'localhost:5500/index.html'
xpath = '//*[@id="testForm"]/textarea'
text = '''
hi
hello
welcome
'''
### CONSTANTS ###

def send_keys_by_line(elmt, text):
    lines = text.strip().split('\n')
    for i, l in enumerate(lines):
        elmt.send_keys(l)
        if i != len(lines)-1:
            elmt.send_keys(Keys.SHIFT, Keys.ENTER)

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get(url)
    textarea = browser.find_element_by_xpath(xpath)
    send_keys_by_line(textarea, text)
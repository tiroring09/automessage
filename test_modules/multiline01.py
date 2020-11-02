'''
multiline test
'''
from selenium import webdriver

# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

url = 'localhost:5500/index.html'
xpath = '//*[@id="testForm"]/textarea'
text = '''
hi
hello
welcome
'''
lines = text.strip().split('\n')

browser = webdriver.Chrome()
browser.get(url)

textarea = browser.find_element_by_xpath(xpath)

for i, l in enumerate(lines):
    textarea.send_keys(l)
    if i != len(lines) - 1:
        textarea.send_keys(Keys.SHIFT, Keys.ENTER)
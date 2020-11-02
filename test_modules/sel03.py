'''
셀레니움 설치 및 최초 실행
config 불러와서 로그인하기
string Template 사용하여 interpolation 이쁘게 하기
'''
from selenium import webdriver
from decouple import config
from time import sleep
from string import Template
from os import listdir
from os.path import join, isfile

#####################CONSTANTS###########################
loginURL = 'https://seller.shopee.sg/account/signin'
searchURL = Template('https://seller.shopee.sg/portal/sale?search=$ORDER_ID')

ID = config('SHOPEE_ID')
PW = config('SHOPEE_PW')

order_id = '201003ABB5626D'

MESSAGE = "Sorry for inconvinience. It's been sent by accident."

WORK_DIR = config('WORK_DIR')
RESULT_DIR = join(WORK_DIR, 'preprocess')

IMG_NAME = 'find_element.png'
IMG_FULL = join(WORK_DIR, IMG_NAME)
#####################CONSTANTS###########################END

def load_preprocessed_images_group(RESULT_DIR):
    # RESULT_DIR로부터 확장자가 jpg인 파일 목록을 정렬하여 불러온다
    filelist = sorted([f for f in listdir(RESULT_DIR) if isfile(join(RESULT_DIR, f)) and f.split('.')[-1] == 'jpg'])

    # 언더바가 없으면 새로운 그룹이고, 언더바가 있으면 기존 그룹에 추가
    filegroup = []
    for f in filelist:
        if '_' in f:
            filegroup[-1].append(f)
        else:
            newgroup = [f]
            filegroup.append(newgroup)
    
    return filegroup

# 디렉토리로부터 파일목록 로드
ordergroup = load_preprocessed_images_group(RESULT_DIR)

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

for og in ordergroup:
    order_id = og[0].split('.')[0]

    # order id 검색
    browser.get(searchURL.substitute(ORDER_ID = order_id))
    sleep(3)

    # 채팅창 띄우기
    btn_xpath = '//*[@id="app"]/div[2]/div[2]/div/div/div/div/div[3]/div/div[2]/a/div[1]/div[1]/div/div[3]'
    browser.find_element_by_xpath(btn_xpath).click()
    # browser.find_element_by_css_selector('.chat-solid').click()
    sleep(3)

    # 사진 전송
    for img in og:
        img = join(RESULT_DIR, img)
        # img_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div'
        # browser.find_element_by_xpath(img_xpath).click()
        # 사진 전송 폼 pyautogui 사용하기

        # 사진 전송 또 다른 방법
        img_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div/input'
        browser.find_element_by_xpath(img_xpath).send_keys(img)
        sleep(3)

    # 메세지 입력
    # msg_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/div/textarea'
    # browser.find_element_by_xpath(msg_xpath).send_keys(MESSAGE)
    # sleep(3)

    # 전송버튼
    # send_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/div/div'
    # browser.find_element_by_xpath(send_xpath).click()
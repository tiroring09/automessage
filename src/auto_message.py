'''
셀레니움 설치 및 최초 실행
config 불러와서 로그인하기
string Template 사용하여 interpolation 이쁘게 하기
from sel03.py
'''
from selenium import webdriver
from decouple import config
from time import sleep
from string import Template
from os import listdir
from os.path import join, isfile

#####################CONSTANTS###########################
MESSAGE = '''
예시 메세지 입니다.
'''

WORK_DIR = config('WORK_DIR')
RESULT_DIR = join(WORK_DIR, 'preprocess')

# SG, PH, MY, ID 중 하나
TARGET_NATION = config('TARGET_NATION')

NATION = {
    'SG': {
        'HOST': config('SHOPEE_HOST_SINGAPORE'),
        'ID': config('SHOPEE_ID_SINGAPORE'),
        'PW': config('SHOPEE_PW_SINGAPORE'),
    },
    'PH': {
        'HOST': config('SHOPEE_HOST_PHILIPPINE'),
        'ID': config('SHOPEE_ID_PHILIPPINE'),
        'PW': config('SHOPEE_PW_PHILIPPINE'),
    },
    'MY': {
        'HOST': config('SHOPEE_HOST_MALAYSIA'),
        'ID': config('SHOPEE_ID_MALAYSIA'),
        'PW': config('SHOPEE_PW_MALAYSIA'),
    },
    'ID': {
        'HOST': config('SHOPEE_HOST_INDONESIA'),
        'ID': config('SHOPEE_ID_INDONESIA'),
        'PW': config('SHOPEE_PW_INDONESIA'),
    },
}

# searchURL = Template('https://seller.shopee.sg/portal/sale?search=$ORDER_ID')
LOGIN_URL = '/account/signin'
SEARCH_URL = '/portal/sale?search='
#####################CONSTANTS###########################END

def load_preprocessed_image_group(RESULT_DIR):
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
ordergroup = load_preprocessed_image_group(RESULT_DIR)

# 크롬브라우저 열기
browser = webdriver.Chrome()

# 국가를 정하고, 국가에 맞는 주소, 아이디, 비밀번호 로드
TARGET_N = NATION[TARGET_NATION]
loginURL = TARGET_N['HOST'] + LOGIN_URL
searchURL = TARGET_N['HOST'] + SEARCH_URL
ID = TARGET_N['ID']
PW = TARGET_N['PW']

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
sleep(3)

for og in ordergroup:
    order_id = og[0].split('.')[0]

    # order id 검색
    browser.get(searchURL + order_id)
    sleep(3)

    # 채팅창 띄우기
    btn_xpath = '//*[@id="app"]/div[2]/div[2]/div/div/div/div/div[3]/div/div[2]/a/div[1]/div[1]/div/div[3]'
    browser.find_element_by_xpath(btn_xpath).click()
    sleep(3)

    # 사진 전송
    # for img in og:
    #     img = join(RESULT_DIR, img)

    #     img_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div/input'
    #     browser.find_element_by_xpath(img_xpath).send_keys(img)
    #     sleep(3)

    # 메세지 입력
    # msg_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/div/textarea'
    # browser.find_element_by_xpath(msg_xpath).send_keys(MESSAGE)
    # sleep(3)

    # 전송버튼
    # send_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/div/div'
    # browser.find_element_by_xpath(send_xpath).click()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decouple import config
from time import sleep
from string import Template
from os import listdir, remove
from os.path import join, isfile, exists

#####################CONSTANTS###########################
# 이모티콘 쓰면 에러나요!
SG_MESSAGE = '''
✈SHIPPED OUT✈

- Estimated delivery date : OCT 16~23
- Request regarding delivery : Ninja Van(+65 6602 8271)

Thank you so much and hope to meet you again
'''

PH_MESSAGE = '''

'''

MY_MESSAGE = '''

'''

ID_MESSAGE = '''

'''

WORK_DIR = config('WORK_DIR')
ROOT_RESULT_DIR = join(WORK_DIR, 'preprocess')

NATION = {
    'SG': {
        'HOST': config('SHOPEE_HOST_SINGAPORE'),
        'ID': config('SHOPEE_ID_SINGAPORE'),
        'PW': config('SHOPEE_PW_SINGAPORE'),
        'MESSAGE': SG_MESSAGE,
    },
    'PH': {
        'HOST': config('SHOPEE_HOST_PHILIPPINE'),
        'ID': config('SHOPEE_ID_PHILIPPINE'),
        'PW': config('SHOPEE_PW_PHILIPPINE'),
        'MESSAGE': PH_MESSAGE,
    },
    'MY': {
        'HOST': config('SHOPEE_HOST_MALAYSIA'),
        'ID': config('SHOPEE_ID_MALAYSIA'),
        'PW': config('SHOPEE_PW_MALAYSIA'),
        'MESSAGE': MY_MESSAGE,
    },
    'ID': {
        'HOST': config('SHOPEE_HOST_INDONESIA'),
        'ID': config('SHOPEE_ID_INDONESIA'),
        'PW': config('SHOPEE_PW_INDONESIA'),
        'MESSAGE': ID_MESSAGE,
    },
}

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

def send_keys_by_line(elmt, text):
    lines = text.strip().split('\n')
    for i, l in enumerate(lines):
        elmt.send_keys(l)
        if i != len(lines)-1:
            elmt.send_keys(Keys.SHIFT, Keys.ENTER)



# 크롬브라우저 열기
browser = webdriver.Chrome()

# 국가 순회
for TARGET_NATION in NATION.keys():
    RESULT_DIR = join(ROOT_RESULT_DIR, TARGET_NATION)

    # 디렉토리로부터 파일목록 로드
    ordergroup = load_preprocessed_image_group(RESULT_DIR)

    # 국가를 정하고, 국가에 맞는 주소, 로그인 정보 로드
    TARGET_N = NATION[TARGET_NATION]
    loginURL = TARGET_N['HOST'] + LOGIN_URL
    searchURL = TARGET_N['HOST'] + SEARCH_URL
    ID = TARGET_N['ID']
    PW = TARGET_N['PW']
    MESSAGE = TARGET_N['MESSAGE']

    browser.get(loginURL)
    sleep(2)

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

        btn_xpath = '//*[@id="app"]/div[2]/div[2]/div/div/div/div/div[3]/div/div[2]/a/div[1]/div[1]/div/div[3]'
        # 페이지 로딩 제대로 되었는지 체크, 오류시 새로고침 (최대 15회)
        err_cnt = 0
        while True:
            try:
                browser.find_element_by_xpath(btn_xpath)
            except:
                browser.refresh()
                sleep(3)
                err_cnt += 1
                if err_cnt > 15:
                    raise Exception('페이지 새로고침 제한 초과: ' + str(err_cnt))
            else:
                break

        # 채팅창 띄우기
        browser.find_element_by_xpath(btn_xpath).click()
        sleep(2)

        # 사진 전송
        for img in og:
            img = join(RESULT_DIR, img)

            img_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div/input'
            browser.find_element_by_xpath(img_xpath).send_keys(img)
            sleep(2)

        # 사진전송 완료시 해당 파일 삭제
        for img in og:
            img = join(RESULT_DIR, img)
            if exists(img):
                remove(img)

        # 메세지 입력
        msg_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/div/textarea'
        message_elmt = browser.find_element_by_xpath(msg_xpath)
        send_keys_by_line(message_elmt, MESSAGE)
        sleep(2)

        # 전송버튼
        send_xpath = '//*[@id="shopee-mini-chat-embedded"]/div[1]/div[2]/div[1]/div[3]/div/div/div[1]/div/div'
        browser.find_element_by_xpath(send_xpath).click()
        sleep(2)
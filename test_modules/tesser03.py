'''
tesseract로 이미지로부터 텍스트 파싱하기
모듈화 도전
'''

from PIL import Image
import pytesseract
from os import listdir
from os.path import join, isfile
import sys
import io
from cross_check01 import cross_check_in_excel

###################### CONSTANTS ######################
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

# IMG = 'find_element.png'
WORKDIR = r'C:\Users\multicampus\Documents\SANDBOX\barcode_reader\샘플사진\preprocess'
IMG = r'20201011_211209.jpg'

FILTER = 'Order'
ORDER_ID_LENGTH = 14
###################### CONSTANTS ###################### END

def find_orderid_from_image(DIR=WORKDIR, IMG=IMG):
    FULL_PATH = join(DIR, IMG)

    # 이미지로부터 문자열 추출
    with Image.open(FULL_PATH) as img:
        raw_text = pytesseract.image_to_string(img)

    # 추출한 문자열 라인 분리
    raw_line = raw_text.splitlines()

    # 공백라인 제거
    line = [ rl.strip() for rl in raw_line if len(rl.strip()) > 1 ]

    # order_id 들어있는 라인 추출
    target_line = [ l for l in line if FILTER in l ]
    target_line = '' if len(target_line) == 0 else target_line[0]

    # target_line에서 단어 길이가 14개면 order_id의 값임
    target = [ word for word in target_line.split(' ') if len(word) == ORDER_ID_LENGTH ]
    target = '' if len(target) == 0 else target[0]

    # logging
    payload = {}
    payload['origin_file'] = IMG.split('.')[0]
    payload['full_text'] = raw_text     # 얘는 디버깅 빡세게할때 쓸라고
    payload['line_filtered'] = target_line
    payload['order_id'] = target

    return payload

if __name__ == '__main__':
    WORKDIR = r'C:/Users/multicampus/Documents/SANDBOX/barcode_reader/샘플사진'

    filelist = [ f for f in listdir(WORKDIR) if isfile(join(WORKDIR, f)) and f.split('.')[-1] == 'jpg' ]

    true_cnt = 0
    orderid_list = []
    for i,f in enumerate(filelist):
        order = find_orderid_from_image(WORKDIR, f)
        order = cross_check_in_excel(WORKDIR, order)

        orderid_list.append(order)

        if len(order['order_id']) != 0:
            print(f"#{ i+1 }: { order['origin_file'] }/// { order['order_id'] } /// { order['cross_check'] }")
        else:
            print(f"#{ i+1 }: { order['origin_file'] }/// { order['line_filtered'] } /// { order['cross_check'] }")

        true_cnt += 1 if order['cross_check'] else 0

    print(true_cnt)
    # return orderid_list
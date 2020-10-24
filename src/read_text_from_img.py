'''
tesseract로 이미지로부터 텍스트 파싱하기
from tessor03.py
'''

from PIL import Image
import pytesseract
from os import listdir
from os.path import join, isfile
import sys
import io
from decouple import config

###################### CONSTANTS ######################
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

pytesseract.pytesseract.tesseract_cmd = config('TESSERACT_PATH')

FILTER = 'Order'
ORDER_ID_LENGTH = 14
###################### CONSTANTS ###################### END

def find_orderid_from_image(DIR, IMG):
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

    # 작업결과 logging
    payload = {}
    payload['origin_file'] = IMG.split('.')[0]
    payload['line_filtered'] = target_line
    payload['order_id'] = target
    # payload['full_text'] = raw_text     # 얘는 디버깅 빡세게할때 쓸라고

    return payload
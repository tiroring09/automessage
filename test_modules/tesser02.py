'''
tesseract로 이미지로부터 텍스트 파싱하기 심화
'''

from PIL import Image
import pytesseract

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

###################### CONSTANTS ######################
# IMG = 'find_element.png'
IMG = r'C:\Users\multicampus\Documents\SANDBOX\barcode_reader\샘플사진\preprocess\20201011_211209.jpg'

FILTER_KWRDS = ['Order', 'Order ID']
ORDER_ID_LENGTH = 14
###################### CONSTANTS ###################### END

# 이미지로부터 문자열 추출
with Image.open(IMG) as img:
    raw_text = pytesseract.image_to_string(img)

# 추출한 문자열 라인 분리
raw_line = raw_text.splitlines()

# 공백라인 제거
line = [ rl.strip() for rl in raw_line if len(rl.strip()) > 1 ]

# for i, l in enumerate(line):
#     print(f"#{i}: [{len(l)}] {l.replace(' ', '.')}")

# order_id 들어있는 라인 추출
target_line = None
for l in line:
    if FILTER_KWRDS[0] in l:
        target_line = l
        break

# order_id에서 길이가 14개면 order_id의 값임
target = None
for word in target_line.split(' '):
    if len(word) == ORDER_ID_LENGTH:
        target = word
        break

print(target)
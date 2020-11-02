'''
tesseract로 이미지로부터 텍스트 파싱하기
https://pypi.org/project/pytesseract

인코딩 에러 해결 레퍼런스: 
https://hugssy.tistory.com/197
'''

from PIL import Image
import pytesseract

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# IMG = 'find_element.png'
IMG = r'C:\Users\multicampus\Documents\SANDBOX\barcode_reader\샘플사진\preprocess\20201011_211209.jpg'

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

data = pytesseract.image_to_string(Image.open(IMG))

print(data)
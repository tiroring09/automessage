'''
이미지로부터 바코드 데이터 읽기
'''

from pyzbar.pyzbar import decode
from PIL import Image

SOURCE = '샘플사진/20201011_211209.jpg'
# SOURCE = 'test.bmp'

_data = decode(Image.open(SOURCE))

for d in _data:
    print(d)
    print(d.data.decode('utf-8'))   # SG2075937643195
    print(d.type)   # CODE128
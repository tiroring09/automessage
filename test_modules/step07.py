'''
step05에서 바코드 읽는 것만 다시 확인
'''
from os import listdir, makedirs
from os.path import isfile, join, exists
from shutil import copyfile
from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd

WORKDIR = 'C:/Users/multicampus/Documents/SANDBOX/barcode_reader/샘플사진'

filelist = [f for f in listdir(WORKDIR) if isfile(join(WORKDIR, f)) and f.split('.')[-1] == 'jpg']

print(len(filelist))

cnt = 0
for f in filelist:
    SOURCE = join(WORKDIR, f)
    _data = decode(Image.open(SOURCE))
    if len(_data) != 0:
        print(_data)
        cnt += 1

print(cnt)

# 16 / 81
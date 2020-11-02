'''
작업 디렉토리로부터 이미지 파일 순회
이미지에서 바코드를 읽는다 >> tracking code
엑셀에서 tcode로부터 order_id를 읽는다 (못찾는 경우, 이미지로부터 tcode를 잘못 읽은 것)
파일명을 order_id로 바꾼다
'''

from os import listdir, makedirs
from os.path import isfile, join, exists
from shutil import copyfile
from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd

'Order.toship.20201009_20201010.xls'
WORKDIR = 'C:/Users/multicampus/Documents/SANDBOX/barcode_reader/샘플사진'
RESULT_DIR = 'preprocess'
LOGGER = []

# 작업 디렉토리로부터 이미지파일 목록과 엑셀파일명 추출
filelist = [f for f in listdir(WORKDIR) if isfile(join(WORKDIR, f)) and f.split('.')[-1] == 'jpg']
excelfile = [f for f in listdir(WORKDIR) if isfile(join(WORKDIR, f)) and f.split('.')[-1] in ['xls']][0]

def TN_to_OID(TN):
    EXCEL = join(WORKDIR, excelfile)
    df = pd.read_excel(EXCEL)
    condition = df['Tracking Number'] == TN
    row = df[condition].reset_index()
    result = row['Order ID'][0]
    return result

# 결과물 디렉토리 생성
if not exists(join(WORKDIR, RESULT_DIR)):
    makedirs(join(WORKDIR, RESULT_DIR))

for f in filelist:
    LOG = {}
    LOG['raw_file'] = f

    SOURCE = join(WORKDIR, f)
    _data = decode(Image.open(SOURCE))
    for d in _data:
        TN = d.data.decode('utf-8') # Tracking Number
        if d.type == 'CODE128' and TN[:2] in ['SG', 'MY']:
            OID = ''
            try:
                OID = TN_to_OID(TN)
            except:
                pass

            dst = join(WORKDIR, RESULT_DIR, OID + '.jpg')
            copyfile(SOURCE, dst)

            LOG['Tracking Number'] = TN
            LOG['Order ID'] = OID

            LOGGER.append(LOG)

for l in LOGGER:
    print(l)

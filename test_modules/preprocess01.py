'''
전처리: 이미지로부터 order_id를 읽고, 엑셀파일과 크로스체킹하여 전처리
'''
from os import listdir, makedirs
from os.path import join, isfile, exists
from shutil import copyfile
from datetime import datetime

from tesser03 import find_orderid_from_image
from cross_check01 import cross_check_in_excel

###################### CONSTANTS ######################

WORKDIR = r'C:\Users\multicampus\Documents\SANDBOX\barcode_reader\샘플사진'
RESULT_DIR = join(WORKDIR, 'preprocess')

###################### CONSTANTS ###################### END

# 작업폴더로부터 사진파일 목록 추출
img_list = [ f for f in listdir(WORKDIR) if isfile(join(WORKDIR, f)) and f.split('.')[-1] == 'jpg' ]

# 이미지로부터 order_id 텍스트 파싱 및 엑셀 크로스체크
orderid_list = []
for i, img in enumerate(img_list):
    order = find_orderid_from_image(WORKDIR, img)
    order = cross_check_in_excel(WORKDIR, order)
    order['no'] = (i+1)

    orderid_list.append(order)

# 전처리 작업 결과물 디렉토리 생성
if not exists(RESULT_DIR):
    makedirs(RESULT_DIR)

# 파일 복붙
for order in orderid_list:

    # 파일명 중복 체크
    name = order['order_id'] if order['cross_check'] else order['origin_file']
    name += '.jpg'

    cnt = 1
    while name in listdir(RESULT_DIR):
        cnt += 1
        name = f"{order['order_id']}_{cnt}.jpg"
    # 파일명 중복 체크 끝

    reading = join(WORKDIR, order['origin_file'] + '.jpg')
    writing = join(RESULT_DIR, name)
    copyfile(reading, writing)

# 로그파일 생성
n = datetime.now()
logger_name = f'log_{n.month}{n.day}_{n.hour}{n.minute}.txt'
logger = join(RESULT_DIR, logger_name)
with open(logger, 'w') as log:
    log.write('========== success ==========\n')
    
    for o in orderid_list:
        if o['cross_check']:
            line = f"#{o['no']} FROM {o['origin_file']} TO {o['order_id']}\n"
            log.write(line)
    
    log.write('========== fail ==========\n')
    for o in orderid_list:
        if not o['cross_check']:
            line = f"#{o['no']} {o['origin_file']} FAILED RESULT IN: {o['line_filtered']}\n"
            log.write(line)
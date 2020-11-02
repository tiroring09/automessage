'''
디렉토리 생성전에 이미 존재하는지 체크를 해야 한다
'''

from os import makedirs
from os.path import join, exists

WORKDIR = r'C:\Users\multicampus\Documents\SANDBOX\barcode_reader\샘플사진'
RESULT_DIR = 'preprocess'

if not exists(join(WORKDIR, RESULT_DIR)):
    makedirs(join(WORKDIR, RESULT_DIR))
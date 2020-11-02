'''
디렉토리로부터 파일 리스트 읽기
'''

from os import listdir
from os.path import isfile, join

WORKDIR = 'C:/Users/multicampus/Documents/SANDBOX/barcode_reader/샘플사진'

filelist = [f for f in listdir(WORKDIR) if isfile(join(WORKDIR, f))]

for f in filelist:
    print(f)
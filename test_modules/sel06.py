'''
작업 디렉토리로부터 전처리된 이미지파일 목록 불러오는데
같은 OrderId끼리 그룹화하기
'''
from selenium import webdriver
from decouple import config
from time import sleep
from string import Template
from os import listdir
from os.path import join, isfile

#####################CONSTANTS###########################
# WORKDIR = r'C:\Users\multicampus\Documents\SANDBOX\barcode_reader\샘플사진'
WORKDIR = config('WORK_DIR')
RESULT_DIR = join(WORKDIR, 'preprocess')
#####################CONSTANTS###########################END

def load_preprocessed_images_group(RESULT_DIR):
    # RESULT_DIR로부터 확장자가 jpg인 파일 목록을 정렬하여 불러온다
    filelist = sorted([f for f in listdir(RESULT_DIR) if isfile(join(RESULT_DIR, f)) and f.split('.')[-1] == 'jpg'])

    # 언더바가 없으면 새로운 그룹이고, 언더바가 있으면 기존 그룹에 추가
    filegroup = []
    for f in filelist:
        if '_' in f:
            filegroup[-1].append(f)
        else:
            newgroup = [f]
            filegroup.append(newgroup)
    
    return filegroup

if __name__ == '__main__':
    order_groups = load_preprocessed_images_group(RESULT_DIR)
    for og in order_groups:
        print(og)
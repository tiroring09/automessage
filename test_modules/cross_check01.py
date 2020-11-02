'''
order_id 엑셀파일에서 검색되는지 크로스체크 로직
'''

import pandas as pd
from os import listdir
from os.path import join, isfile

def cross_check_in_excel(DIR, payload):
    # 디렉토리 경로에서 엑셀파일 읽기
    EXCEL = [ f for f in listdir(DIR) if isfile(join(DIR, f)) and f.split('.')[-1] == 'xls' ]
    EXCEL = None if len(EXCEL) == 0 else EXCEL[0]
    FULL_PATH = join(DIR, EXCEL)

    # 엑셀파일 df로 읽기
    df = pd.read_excel(FULL_PATH)

    # 검색
    order_id = [ payload['order_id'] ]
    condition = df['Order #'].isin(order_id)
    filtered_df = df[condition]

    order_cnt = len(filtered_df)
    cross_check = order_cnt > 0

    # 로깅
    payload['order_cnt_in_excel'] = order_cnt
    payload['cross_check'] = cross_check

    return payload

if __name__ == '__main__':
    WORKDIR = r'C:\Users\multicampus\Documents\SANDBOX\barcode_reader\샘플사진'
    ORDER = { 'order_id' : '20101005QS9WYV', }

    ORDER = cross_check_in_excel(WORKDIR, ORDER)

    print(ORDER['order_id'], ORDER['order_cnt_in_excel'], ORDER['cross_check'])
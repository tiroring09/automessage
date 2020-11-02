'''
엑셀파일 pandas dataframe으로 변환하여 다루기
https://hogni.tistory.com/93
'''

import pandas as pd

df = pd.read_excel('Order.toship.20201009_20201010.xls')

# df = raw.loc[:, ['Order ID', 'Tracking Number']]  # same
# df = raw[['Order ID', 'Tracking Number']]

# result = df.head()
# result = df['Tracking Number'].head()   # 열만 떼어오기

# result = df['Tracking Number'].isin(['SG204959238008Z']).head() # 해당 열에서 특정 문자열 검색
# result = df[df['Tracking Number'] == 'SG204959238008Z']

# Tracking Number에서 특정 문자열을 갖는 행에서 Order ID 추출
# condition = df['Tracking Number'].isin(['SG204959238008Z'])   # same
condition = df['Tracking Number'] == 'SG204959238008Z'
row = df[condition].reset_index()
# result = row.loc[:,'Order ID']
result = row['Order ID'][0]

# get, lookup
# https://kongdols-room.tistory.com/121
# result = df.get('Order Status')

print(result)
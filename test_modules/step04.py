'''
step03에서 했던 dataframe 여러 시도 정리
'''

import pandas as pd

df = pd.read_excel('Order.toship.20201009_20201010.xls')

condition = df['Tracking Number'] == 'SG204959238008Z'
row = df[condition].reset_index()
result = row['Order ID'][0]

print(result)
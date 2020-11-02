'''
.env에서 멀티라인 실험 >> 실패
'''

from decouple import config

text = config('TEXT')
print(text)
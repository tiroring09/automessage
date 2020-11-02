'''
copy a file in Python?
https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
'''
from shutil import copyfile

src = 'README.md'
dst = '샘플사진/RR.md'

copyfile(src, dst)

'''
디렉토리 만들기
'''
import os
if not os.path.exists('my_folder'):
    os.makedirs('my_folder')
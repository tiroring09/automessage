'''
text를 라인으로 분리하기
'''

text = '''
hello
hi
'''

lines = text.strip().split('\n')
# print(lines)
for l in lines:
    print(l)
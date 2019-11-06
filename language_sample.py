import MeCab
import re

filepath = 'C:\\Users\\sachi\\Desktop\\code\\python\\sample.txt'

with open(filepath,'r') as f:
    txt = f.read()

parse = MeCab.Tagger().parse(txt)
lines = parse.split('\n')
items = (re.split('[\t,]', line) for line in lines)

new_list = []

for word in items:
    print(word[0])
    new_list.append(word[0])
print(len(new_list))


with open('C:\\Users\\sachi\\Desktop\\code\\python\\sample_tagger.txt','w') as f1:
    f1.write('これは書き込みのテスト\n')
    for i in range(len(new_list)):
        f1.write('{}\n'.format(new_list[i]))
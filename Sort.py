#Azure上のサーバーでソートアルゴリズムを走らせる
import requests
import random
num = 100
num_list = ''
for i in range(num):
    tmp = random.randint(1, num*10000)
    num_list += str(tmp)
    num_list += ','

url = "https://koheiyamada.azurewebsites.net/api/Sort"

params = {'num_list':num_list,
        'mode':'heap'}

res = requests.get(url, params = params)

print(res.text)
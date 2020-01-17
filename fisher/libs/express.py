# _*_ coding: utf-8 _*_
import json
import requests
from django.conf import settings

from fisher.libs.json_to_obj import complex_dict_to_object

# 独立使用django的model
import sys
import os

#获取当前文件的路径（运行脚本）
pwd = os.path.dirname(os.path.realpath(__file__))
#获取项目的根目录
sys.path.append(pwd+"../")
print(pwd+"../")



def get_express_data(number):
    host = 'https://wuliu.market.alicloudapi.com'
    path = '/kdi'
    # appcode = '62c863d1ae434fed9282b46288032400'
    appcode = settings.EXPRESS_APPCODE
    querys = f'no={number}'
    url = host + path + '?' + querys
    headers = {'Authorization': 'APPCODE ' + appcode}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

if __name__=='__main__':
    print(settings.EXPRESS_APPCODE)
    data = get_express_data(780098068058)
    # express = dict_to_object(data)
    express = complex_dict_to_object(data)
    for x in express.result.list:
        print('x.time',x.time)
        print('x.status',x.status)

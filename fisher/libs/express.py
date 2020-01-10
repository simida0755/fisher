# _*_ coding: utf-8 _*_
import json
import requests
from django.conf import settings

from fisher.templates.express.json_to_obj import complex_dict_to_object


def get_express_data(number):
    host = 'https://wuliu.market.alicloudapi.com'
    path = '/kdi'
    appcode = '62c863d1ae434fed9282b46288032400'
    querys = f'no={number}'
    url = host + path + '?' + querys
    headers = {'Authorization': 'APPCODE ' + appcode}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

if __name__=='__main__':
    data = get_express_data(780098068058)
    express = complex_dict_to_object(data)
    for x in express.result.list:
        print('x.name',x.name)
        print('x.status',x.status)

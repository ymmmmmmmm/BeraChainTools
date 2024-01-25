# -*- coding: cp936 -*-
import requests


#自行定义
def get_proxy():
    proxy_url = ''
    aaa = requests.get(proxy_url).text
    proxy_host = aaa.splitlines()[0]
    print('代理IP为：' + proxy_host)
    proxy = {
        'http': 'http://' + proxy_host,
        'https': 'http://' + proxy_host
    }
    return proxy

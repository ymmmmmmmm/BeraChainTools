# -*- coding: cp936 -*-
import requests


#���ж���
def get_proxy():
    proxy_url = ''
    aaa = requests.get(proxy_url).text
    proxy_host = aaa.splitlines()[0]
    print('����IPΪ��' + proxy_host)
    proxy = {
        'http': 'http://' + proxy_host,
        'https': 'http://' + proxy_host
    }
    return proxy

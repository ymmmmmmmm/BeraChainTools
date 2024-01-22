# -*- coding: utf-8 -*-
# Time     :2024/1/19 21:38
# Author   :ym
# File     :utils.py
import time
from typing import Union

import requests
from loguru import logger


def get_yescaptcha_google_token(yes_captcha_client_key: str) -> Union[bool, str]:
    json_data = {"clientKey": yes_captcha_client_key,
                 "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                          "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                          "type": "RecaptchaV3TaskProxylessM1S7", "pageAction": "submit"}, "softID": 109}
    response = requests.post(url='https://api.yescaptcha.com/createTask', json=json_data).json()
    if response['errorId'] != 0:
        raise ValueError(response)
    task_id = response['taskId']
    time.sleep(5)
    for _ in range(30):
        data = {"clientKey": yes_captcha_client_key, "taskId": task_id}
        response = requests.post(url='https://api.yescaptcha.com/getTaskResult', json=data).json()
        if response['status'] == 'ready':
            return response['solution']['gRecaptchaResponse']
        else:
            time.sleep(2)
    logger.warning(response)
    return False


def get_no_captcha_google_token(no_captcha_api_token: str) -> Union[bool, str]:
    headers = {'User-Token': no_captcha_api_token, 'Content-Type': 'application/json', 'Developer-Id': 'UTtF29'}
    json_data = {'sitekey': "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                 'referer': 'https://artio.faucet.berachain.com/', 'size': 'invisible', 'title': 'Berachain Faucet',
                 'action': 'submit', 'internal': False}
    response = requests.post(url='http://api.nocaptcha.io/api/wanda/recaptcha/universal', headers=headers,
                             json=json_data).json()
    if response.get('status') == 1:
        if response.get('msg') == '验证成功':
            return response['data']['token']
    logger.warning(response)
    return False


def get_2captcha_google_token(captcha_key: str) -> Union[bool, str]:
    params = {'key': captcha_key, 'method': 'userrecaptcha', 'version': 'v3', 'action': 'submit', 'min_score': 0.5,
              'googlekey': '6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH', 'pageurl': 'https://artio.faucet.berachain.com/',
              'json': 1}
    response = requests.get(f'https://2captcha.com/in.php?', params=params).json()
    if response['status'] != 1:
        raise ValueError(response)
    task_id = response['request']
    for _ in range(60):
        response = requests.get(f'https://2captcha.com/res.php?key={captcha_key}&action=get&id={task_id}&json=1').json()
        if response['status'] == 1:
            return response['request']
        else:
            time.sleep(3)
    return False


if __name__ == '__main__':
    # print(get_no_captcha_google_token(''))
    print(get_2captcha_google_token(''))

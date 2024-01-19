# -*- coding: utf-8 -*-
# Time     :2024/1/19 21:38
# Author   :ym
# Email    :49154181@qq.com
# File     :utils.py
import os
import time
from typing import Union

import requests
from dotenv import load_dotenv

load_dotenv()
proxy_url = os.getenv("PROXY_URL")
YesCaptchaClientKey = os.getenv("YesCaptchaClientKey")


def get_ip():
    if proxy_url == 'null':
        return False
    response = requests.get(url=proxy_url).text.strip().replace('\n', '')
    return {"http": f'http://{response}', "https": f'http://{response}'}


def get_google_token() -> Union[bool, str]:
    json_data = {"clientKey": YesCaptchaClientKey,
                 "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                          "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                          "type": "RecaptchaV3TaskProxylessM1S7", "pageAction": "submit"}, "softID": 109}
    response = requests.post(url='https://api.yescaptcha.com/createTask', json=json_data).json()
    if response['errorId'] != 0:
        raise ValueError(response)
    task_id = response['taskId']
    time.sleep(5)
    for _ in range(30):
        data = {"clientKey": YesCaptchaClientKey, "taskId": task_id, }
        response = requests.post(url='https://api.yescaptcha.com/getTaskResult', json=data).json()
        if response['status'] == 'ready':
            return response['solution']['gRecaptchaResponse']
        else:
            time.sleep(2)
    return False


if __name__ == '__main__':
    print(get_google_token())

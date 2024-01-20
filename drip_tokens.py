# -*- coding: utf-8 -*-
# Time     :2024/1/19 21:30
# Author   :ym
# File     :drip_tokens.py
import concurrent.futures
import json
import os

import requests
from dotenv import load_dotenv
from eth_account import Account
from faker import Faker
from loguru import logger

from utils import get_google_token, get_ip

load_dotenv()
max_workers = os.getenv("MaxWorkers")

fake = Faker(locale='zh-CN')


def claim(address=None):
    if not address:
        account = Account.create()
        claim_address = account.address
    else:
        claim_address = address
    while True:
        user_agent = fake.chrome()
        try:
            google_token = get_google_token()
            if not google_token:
                raise ValueError('获取谷歌结果出错')
            headers = {'authority': 'artio-80085-ts-faucet-api-2.berachain.com', 'accept': '*/*',
                       'accept-language': 'zh-CN,zh;q=0.9', 'authorization': f'Bearer {google_token}',
                       'cache-control': 'no-cache', 'content-type': 'text/plain;charset=UTF-8',
                       'origin': 'https://artio.faucet.berachain.com', 'pragma': 'no-cache',
                       'referer': 'https://artio.faucet.berachain.com/', 'user-agent': user_agent}

            params = {'address': claim_address}
            response = requests.post('https://artio-80085-ts-faucet-api-2.berachain.com/api/claim', params=params,
                                     headers=headers, data=json.dumps(params), proxies=get_ip()).json()
            if 'Txhash' in response['msg'] or 'to the queue' in response['msg']:
                logger.success(f'{claim_address}:{response}')
                if not address:
                    with open('bera_claim_success.txt', 'a+') as f:
                        f.writelines(f'{account.address}----{account.key.hex()}\n')
                return
            else:
                logger.warning(f'{claim_address}:{response}')
        except Exception as e:
            logger.error(e)
            logger.exception(e)


def claim_new_address():
    """
    新地址领水
    :return:
    """
    claim_nums = 100
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(claim, None) for i in range(claim_nums + 1)]


def claim_path_address():
    """
    读取指定路径文件地址领水，地址一行一个
    :return:
    """
    address_path = './address.txt'
    with open(address_path, 'r') as f:
        address_list = f.readline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(claim, i.replace('\n', '')) for i in address_list]


if __name__ == '__main__':
    claim_new_address()
    # claim_path_address()

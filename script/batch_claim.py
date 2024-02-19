# -*- coding: utf-8 -*-
# Time     :2024/1/25 03:15
# Author   :ym
# File     :batch_claim.py
import asyncio
import json
from typing import Union

import aiofiles
import aiohttp
from eth_typing import ChecksumAddress, Address
from faker import Faker
from loguru import logger

fake = Faker()


async def get_2captcha_google_token(session: aiohttp.ClientSession) -> Union[bool, str]:
    params = {'key': client_key, 'method': 'userrecaptcha', 'version': 'v3', 'action': 'submit', 'min_score': 0.5,
              'googlekey': '6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH', 'pageurl': 'https://artio.faucet.berachain.com/',
              'json': 1}
    async with session.get('https://2captcha.com/in.php?', params=params) as response:
        response_json = await response.json()
        # logger.debug(response_json)
        if response_json['status'] != 1:
            logger.warning(response_json)
            return False
        task_id = response_json['request']
    for _ in range(120):
        async with session.get(
                f'https://2captcha.com/res.php?key={client_key}&action=get&id={task_id}&json=1') as response:
            response_json = await response.json()
            if response_json['status'] == 1:
                return response_json['request']
            else:
                await asyncio.sleep(1)
    return False


async def get_2captcha_turnstile_token(session: aiohttp.ClientSession) -> Union[bool, str]:
    params = {'key': client_key, 'method': 'turnstile',
              'sitekey': '0x4AAAAAAARdAuciFArKhVwt',
              'pageurl': 'https://artio.faucet.berachain.com/',
              'json': 1}
    async with session.get('https://2captcha.com/in.php?', params=params) as response:
        response_json = await response.json()
        # logger.debug(response_json)
        if response_json['status'] != 1:
            logger.warning(response_json)
            return False
        task_id = response_json['request']
    for _ in range(120):
        async with session.get(
                f'https://2captcha.com/res.php?key={client_key}&action=get&id={task_id}&json=1') as response:
            response_json = await response.json()
            if response_json['status'] == 1:
                return response_json['request']
            else:
                await asyncio.sleep(1)
    return False


async def get_yescaptcha_google_token(session: aiohttp.ClientSession) -> Union[bool, str]:
    json_data = {"clientKey": client_key,
                 "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                          "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                          "type": "RecaptchaV3TaskProxylessM1S7", "pageAction": "submit"}, "softID": 109}
    async with session.post('https://api.yescaptcha.com/createTask', json=json_data) as response:
        response_json = await response.json()
        if response_json['errorId'] != 0:
            logger.warning(response_json)
            return False
        task_id = response_json['taskId']
    for _ in range(120):
        data = {"clientKey": client_key, "taskId": task_id}
        async with session.post('https://api.yescaptcha.com/getTaskResult', json=data) as response:
            response_json = await response.json()
            if response_json['status'] == 'ready':
                return response_json['solution']['gRecaptchaResponse']
            else:
                await asyncio.sleep(1)
    return False


async def get_yescaptcha_turnstile_token(session: aiohttp.ClientSession) -> Union[bool, str]:
    json_data = {"clientKey": client_key,
                 "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                          "websiteKey": "0x4AAAAAAARdAuciFArKhVwt",
                          "type": "TurnstileTaskProxylessM1"}, "softID": 109}
    async with session.post('https://api.yescaptcha.com/createTask', json=json_data) as response:
        response_json = await response.json()
        if response_json['errorId'] != 0:
            logger.warning(response_json)
            return False
        task_id = response_json['taskId']
    for _ in range(120):
        data = {"clientKey": client_key, "taskId": task_id}
        async with session.post('https://api.yescaptcha.com/getTaskResult', json=data) as response:
            response_json = await response.json()
            if response_json['status'] == 'ready':
                return response_json['solution']['token']
            else:
                await asyncio.sleep(1)
    return False


async def get_ez_captcha_google_token(session: aiohttp.ClientSession) -> Union[bool, str]:
    json_data = {
        "clientKey": client_key, "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                                          "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                                          "type": "ReCaptchaV3TaskProxyless"}, "appId": "34119"}
    async with session.post('https://api.ez-captcha.com/createTask', json=json_data) as response:
        response_json = await response.json()
        if response_json['errorId'] != 0:
            logger.warning(response_json)
            return False
        task_id = response_json['taskId']
    for _ in range(120):
        data = {"clientKey": client_key, "taskId": task_id}
        async with session.post('https://api.ez-captcha.com/getTaskResult', json=data) as response:
            response_json = await response.json()
            if response_json['status'] == 'ready':
                return response_json['solution']['gRecaptchaResponse']
            else:
                await asyncio.sleep(1)
    return False


async def get_ip(session: aiohttp.ClientSession) -> str:
    async with session.get(get_ip_url) as response:
        response_text = await response.text()
    # proxy 格式 : 'http://user:password@ip:port' or 'http://ip:port'
    return f'http://{response_text.strip()}'


async def write_to_file(address: Union[Address, ChecksumAddress]):
    async with aiofiles.open('claim_success.txt', 'a+') as f:
        await f.write(f'{address}\n')


async def read_to_file(file_path: str):
    async with aiofiles.open('./claim_success.txt', 'r') as success_file:
        claim_success = await success_file.read()

    async with aiofiles.open(file_path, 'r') as file:
        lines = await file.readlines()
    claim_list = [_address.strip() for _address in lines if _address.strip() not in claim_success]

    return claim_list


async def claim_faucet(address: Union[Address, ChecksumAddress], google_token: str, session: aiohttp.ClientSession):
    user_agent = fake.chrome()
    headers = {'authority': 'artio-80085-ts-faucet-api-2.berachain.com', 'accept': '*/*',
               'accept-language': 'zh-CN,zh;q=0.9', 'authorization': f'Bearer {google_token}',
               'cache-control': 'no-cache', 'content-type': 'text/plain;charset=UTF-8',
               'origin': 'https://artio.faucet.berachain.com', 'pragma': 'no-cache',
               'referer': 'https://artio.faucet.berachain.com/', 'user-agent': user_agent}
    params = {'address': address}
    proxies = await get_ip(session)
    async with session.post('https://artio-80085-faucet-api-cf.berachain.com/api/claim', headers=headers,
                            data=json.dumps(params), params=params, proxy=proxies) as response:
        response_text = await response.text()
    if 'try again' not in response_text and 'message":"' in response_text:
        logger.success(response_text)
        await write_to_file(address)
    elif 'Txhash' in response_text:
        logger.success(response_text)
        await write_to_file(address)
    else:
        logger.warning(response_text.replace('\n', ''))


def get_solver_provider():
    provider_dict = {'yescaptcha': get_yescaptcha_turnstile_token, '2captcha': get_2captcha_turnstile_token}
    if solver_provider not in list(provider_dict.keys()):
        raise ValueError("solver_provider must be 'yescaptcha'")
    return provider_dict[solver_provider]


async def claim(address: Union[Address, ChecksumAddress], session: aiohttp.ClientSession):
    try:
        google_token = await get_solver_provider()(session)
        if google_token:
            await claim_faucet(address, google_token, session)
    except Exception as e:
        logger.warning(f'{address}:{e}')


async def run(file_path):
    sem = asyncio.Semaphore(max_concurrent)
    address_list = await read_to_file(file_path)
    async with aiohttp.ClientSession() as session:
        async def claim_wrapper(address):
            async with sem:
                await claim(address, session)

        await asyncio.gather(*[claim_wrapper(address) for address in address_list])


if __name__ == '__main__':
    """
    如果你不能完全的读懂代码，不建议直接运行本程序避免造成损失
    运行时会读取当前文件夹下的claim_success.txt文本，跳过已经成功的地址
    单进程性能会有瓶颈,大概一分钟能领1000左右,自行套多进程或复制多开
    """
    # 验证平台key
    client_key = 'xxxxxxxxxxx'
    # 目前支持使用yescaptcha 2captcha
    solver_provider = 'yescaptcha'
    # 代理获取链接 设置一次提取一个 返回格式为text
    get_ip_url = 'http://127.0.0.1:8883/get_ip'
    # 并发数量
    max_concurrent = 128
    # 读取文件的路径 地址一行一个
    _file_path = './address.txt'
    asyncio.run(run(_file_path))

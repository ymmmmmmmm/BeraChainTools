# -*- coding: utf-8 -*-
# Time     :2024/1/25 03:15
# Author   :ym
# File     :batch_claim.py
import asyncio
import json
import random
import time
# 在代码中添加计时装饰器
from functools import wraps
from typing import Union

import aiofiles
import aiohttp
from eth_typing import ChecksumAddress, Address
from faker import Faker
from loguru import logger

from script.example.google_token import get_yescaptcha_turnstile_token
from script.example.operator_record import record_success_operator_address, record_today_file_path, file_lines
from script.example.wallet_helper import parse_line, read_address_from_file

fake = Faker()
# 并发数量
max_concurrent = 128
operate = 'claim_faucet'


def fibonacci_sequence(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence


async def get_ip_with_retry(session, max_retries=3):
    for attempt in range(1, max_retries + 1):
        proxies = await get_ip(session)
        if '提取频率太高，请稍后再试' in proxies:
            print(f"第 {attempt} 次获取代理 IP 失败：频率太高，请稍后再试。")

            # 计算斐波那契数列作为延迟
            delay = fibonacci_sequence(attempt)[-1]  # 取斐波那契数列的最后一个值
            print(f"等待 {delay} 秒后重试...")
            await asyncio.sleep(delay)
        else:
            return proxies

    raise ValueError(f"无法获取代理 IP，已达到最大重试次数。")


def timing_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds to run")
        return result

    return wrapper


@timing_decorator
async def claim_faucet(address: Union[Address, ChecksumAddress], google_token: str, session: aiohttp.ClientSession):
    user_agent = fake.chrome()
    headers = {'authority': 'artio-80085-ts-faucet-api-2.berachain.com', 'accept': '*/*',
               'accept-language': 'zh-CN,zh;q=0.9', 'authorization': f'Bearer {google_token}',
               'cache-control': 'no-cache', 'content-type': 'text/plain;charset=UTF-8',
               'origin': 'https://artio.faucet.berachain.com', 'pragma': 'no-cache',
               'referer': 'https://artio.faucet.berachain.com/', 'user-agent': user_agent}
    params = {'address': address}
    proxies = await get_ip_with_retry(session)
    logger.warning(f'ip : {proxies}')
    async with session.post('https://artio-80085-faucet-api-cf.berachain.com/api/claim', headers=headers,
                            data=json.dumps(params), params=params, proxy=proxies) as response:
        response_text = await response.text()
    if 'try again' not in response_text and 'message":"' in response_text:
        logger.success(response_text)
        await record_success_operator_address(address, 'claim_faucet')
    elif 'Txhash' in response_text:
        logger.success(response_text)
        await record_success_operator_address(address, 'claim_faucet')
    else:
        logger.warning(response_text.replace('\n', ''))


@timing_decorator
async def claim(address: Union[Address, ChecksumAddress], session: aiohttp.ClientSession):
    try:
        google_token = await get_yescaptcha_turnstile_token(session)
        if google_token:
            await claim_faucet(address, google_token, session)
    except Exception as e:
        logger.warning(f'{address}:{e}')


@timing_decorator
async def run():
    sem = asyncio.Semaphore(max_concurrent)
    success_addresses = read_address_from_file(record_today_file_path('claim_faucet'))
    claim_list = await filter_wallets(success_addresses)
    logger.debug(f'address remain to run {len(claim_list)}')
    async with aiohttp.ClientSession() as session:
        async def claim_wrapper(address):
            async with sem:
                await claim(address, session)

        await asyncio.gather(*[claim_wrapper(wallet) for wallet in claim_list])


@timing_decorator
async def filter_wallets(success_address: list):
    async with aiofiles.open('./example/account/accounts.txt', 'r') as file:
        lines = await file.readlines()
        origin_wallet = []
        claim_list = []
        for line in lines:
            wallet = parse_line(line)
            origin_wallet.append(wallet)
    claim_list = [wallet.address.strip() for wallet in origin_wallet if
                  wallet.address.strip('\'') not in success_address]

    return claim_list


@timing_decorator
async def get_ip(session: aiohttp.ClientSession) -> str:
    delay = random.uniform(0, 0.5)
    await asyncio.sleep(delay)
    async with session.get(get_ip_url) as response:
        response_text = await response.text()
    # proxy 格式 : 'http://user:password@ip:port' or 'http://ip:port'
    return f'http://{response_text.strip()}'


def worker():
    today_success_file_path = record_today_file_path(operate)
    success_count = file_lines(today_success_file_path)
    total_count = file_lines('./example/account/accounts.txt')
    round = 0
    limit = 1
    while success_count < total_count:
        logger.debug(f'start round -> {round}')
        if round == limit:
            logger.debug(f'tried {limit} times, quit')
            break
        asyncio.run(run())
        success_count = file_lines(today_success_file_path)
        logger.debug(
            f'totalCount = {total_count}, success_count = {success_count}, rate = {success_count / total_count}')
        round += 1


if __name__ == '__main__':
    """
    如果你不能完全的读懂代码，不建议直接运行本程序避免造成损失
    运行时会读取当前文件夹下的claim_success.txt文本，跳过已经成功的地址
    单进程性能会有瓶颈,大概一分钟能领1000左右,自行套多进程或复制多开
    """
    # 代理获取链接 设置一次提取一个 返回格式为text
    get_ip_url = '换成你的自己的从https://www.rola-ip.co/获取的动态 ip 获取链接'
    worker()
    # asyncio.run(record_success_operator_address('2323', '22'))

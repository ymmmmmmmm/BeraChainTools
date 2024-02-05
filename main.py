import random
import os
import time
import configparser
from eth_account import Account
from loguru import logger

from utils.bend_interaction_utils import bend_interacte
from utils.bex_interaction_utils import bex_interacte
from utils.deploy_contract import deploy_contract
from utils.honey_interaction_utils import honey_interacte
from utils.honeyjar_interaction_utils import honeyjar_interacte
from utils.waters_utils import generate_wallet
from bera_tools import BeraChainTools
from utils.waters_utils import get_proxy


def interacte(private_key, rpc_url, proxy_url, solver_provider, client_key):
    # step1: 领水
    bera = BeraChainTools(private_key=private_key, client_key=client_key, solver_provider=solver_provider,
                          rpc_url=rpc_url)
    for i in range(3):
        balance = bera.get_balance()
        print("测试币余额", balance)
        if balance == 0:
            try:
                result = bera.claim_bera(proxies=get_proxy(proxy_url))
                logger.debug(f'{result.text}\n')
                time.sleep(4)
                break
            except Exception as e:
                print(e)
                time.sleep(4)
        else:
            break

    balance = bera.get_balance()
    if balance > 0:
        bex_interacte(private_key, rpc_url)
        steps = [
            honey_interacte,
            bend_interacte,
            honeyjar_interacte,
            deploy_contract
        ]
        random.shuffle(steps)
        for step in steps:
            step(private_key, rpc_url)


if __name__ == '__main__':
    # 是否为初始化钱包模式
    mode_init_wallet = False
    config = configparser.ConfigParser()
    config.read('config.ini')
    file_path = config.get('app', 'file_path')
    rpc_url = config.get('app', 'rpc_url')
    proxy_url = config.get('app', 'proxy_url')
    solver_provider = config.get('app', 'solver_provider')
    client_key = config.get('app', 'client_key')
    # 如果私钥文件,自动创建一个
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write('')
    if mode_init_wallet:
        generate_wallet(1, rpc_url, proxy_url, solver_provider, client_key, file_path)
    else:
        interaction_count = 0  # 初始化交互计数器
        with open(file_path, 'r') as file:

            # 逐行读取文件
            k = 0
            for private_key in file:
                k += 1
                if k > 0:
                    interaction_count += 1  # 每次开始交互时增加计数器
                    account = Account.from_key(private_key.strip())
                    logger.debug(
                        f'第{++interaction_count}次开始交互，账户地址为：{account.address}，账户私钥为：{private_key.strip()}')
                    start_time = time.time()
                    interacte(private_key.strip(), rpc_url, proxy_url, solver_provider, client_key)
                    end_time = time.time()
                    logger.success(f'交互完成，账户为：{private_key.strip()},用时:{end_time-start_time}')
                    logger.debug('\n\n\n\n\n')

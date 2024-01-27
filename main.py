import random
import configparser
from eth_account import Account
from loguru import logger

from utils.bend_interaction_utils import bend_interacte
from utils.bex_interaction_utils import bex_interacte
from utils.deploy_contract import deploy_contract
from utils.honey_interaction_utils import honey_interacte
from utils.honeyjar_interaction_utils import honeyjar_interacte
from utils.waters_utils import generate_wallet


def interacte(private_key):
    # step1: 领水

    # setp2 Bex 交互
    bex_interacte(private_key)

    # setp3 Honey 交互
    # honey_interacte(private_key)

    # step4 Bend 交互
    # bend_interacte(private_key)

    # step5 0xhoneyjar 交互
    # honeyjar_interacte(private_key)

    # setp6 部署合约
    # deploy_contract(private_key)

    steps = [honey_interacte, bend_interacte, honeyjar_interacte, deploy_contract]
    random.shuffle(steps)

    for step in steps:
        step(private_key)


if __name__ == '__main__':
    # 是否为初始化钱包模式
    mode_init_wallet = True
    config = configparser.ConfigParser()
    config.read('config.ini')
    file_path = config.get('app', 'file_path')
    if mode_init_wallet:
        rpc_url = config.get('app', 'rpc_url')
        proxy_url = config.get('app', 'proxy_url')
        solver_provider = config.get('app', 'solver_provider')
        client_key = config.get('app', 'client_key')
        generate_wallet(200, rpc_url, proxy_url, solver_provider, client_key, file_path)
    else:
        interaction_count = 0  # 初始化交互计数器
        with open(file_path, 'r') as file:
            # 逐行读取文件
            for private_key in file:
                account = Account.from_key(private_key.strip())
                interaction_count += 1  # 每次开始交互时增加计数器
                logger.debug(
                    f'第{++interaction_count}次开始交互，账户地址为：{account.address}，账户私钥为：{private_key.strip()}')
                interacte(private_key.strip())
                logger.success(f'交互完成，账户为：{private_key.strip()}')
                logger.debug('\n\n\n\n\n')

import random
import string
import time

from eth_account import Account
from loguru import logger
from solcx import install_solc

from bera_tools import BeraChainTools


def deploy_contract(private_key):
    for _ in range(10):
        if deploy_contract_(private_key):
            return


def deploy_contract_(private_key):
    try:
        account = Account.from_key(private_key)
        bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')
        # 安装0.4.18 版本编译器
        install_solc('0.4.18')
        # 读取sol文件
        with open('./config/WETH.sol', 'r') as f:
            code = f.read()
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        code = code.replace('Bera Test Ether', 'Bera Test Ether' + random_string)
        # 部署合约
        result = bera.deploy_contract(code, '0.4.18')
        # logger.debug(result)
        logger.success(f'部署合约成功,{result}')
        logger.debug('-------------------------------------------------------------------------------------')
        return True
    except Exception as e:
        logger.error(f'部署合约失败，{e}')
        time.sleep(5)
    return False

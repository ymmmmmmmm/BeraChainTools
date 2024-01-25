from eth_account import Account
from loguru import logger

from utils.bend_interaction_utils import bend_interacte
from utils.bex_interaction_utils import bex_interacte
from utils.deploy_contract import deploy_contract
from utils.honey_interaction_utils import honey_interacte
from utils.honeyjar_interaction_utils import honeyjar_interacte


def interacte(private_key):
    # step1: 领水

    # setp2 Bex 交互
    bex_interacte(private_key)

    # setp3 Honey 交互
    honey_interacte(private_key)

    # step4 Bend 交互
    bend_interacte(private_key)

    # step5 0xhoneyjar 交互
    honeyjar_interacte(private_key)

    # setp6 部署合约
    deploy_contract(private_key)


if __name__ == '__main__':
    file_path = './wallet/bera_private_keys.txt'  # 请替换为您的文件路径
    with open(file_path, 'r') as file:
        # 逐行读取文件
        for private_key in file:
            account = Account.from_key(private_key.strip())
            logger.debug(f'开始交互，账户地址为{account.address}，账户私钥为：{private_key.strip()}')
            interacte(private_key.strip())
            logger.success(f'交互完成，账户为：{private_key.strip()}')
            logger.debug('\n\n\n\n\n')

from loguru import logger
from solcx import install_solc

from bera_tools import BeraChainTools


def deployment(account):
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    # 安装0.4.18 版本编译器
    install_solc('0.4.18')
    # 读取sol文件
    with open('config/WETH.sol', 'r') as f:
        code = f.read()
    # 部署合约
    result = bera.deploy_contract(code, '0.4.18')
    logger.debug(result)

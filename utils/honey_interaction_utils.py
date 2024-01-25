import time

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import honey_swap_address, usdc_address, honey_address


def honey_interacte(private_key):
    for _ in range(10):
        if honey_interacte_(private_key):
            return


def honey_interacte_(private_key):
    account = Account.from_key(private_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    try:
        # 授权usdc
        logger.debug('STGUSDC转换HONEY开始')
        approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
        # logger.debug(approve_result)

        # 使用usdc mint honey
        usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
        result = bera.honey_mint(int(usdc_balance * 0.5))
        # logger.debug(result)
        logger.success(f'STGUSDC转换HONEY成功,{result}')

        logger.debug('HONEY转换STGUSDC开始')
        # 授权honey
        approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
        # logger.debug(approve_result)
        # 赎回
        honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
        result = bera.honey_redeem(int(honey_balance * 0.5))
        # logger.debug(result)
        logger.success(f'HONEY转换STGUSDC成功,赎回成功！！！,{result}')
        logger.debug('-------------------------------------------------------------------------------------')
        return True
    except Exception as e:
        logger.error(e)
        time.sleep(5)
        return False

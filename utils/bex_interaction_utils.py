from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import (
    usdc_address, wbear_address, weth_address, bex_approve_liquidity_address,
    usdc_pool_liquidity_address, weth_pool_liquidity_address
)


def bex_interacte(private_key):
    logger.debug('开始Bex 交互')

    account = Account.from_key(private_key)
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    try:
        # bex 使用bera交换usdc
        bera_balance = bera.w3.eth.get_balance(account.address)
        result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, usdc_address)
        logger.success(f'bex 使用bera交换usdc成功！！！,{result}')
    except Exception as e:
        logger.error(f'bex 使用bera交换usdc失败！！！,{e}')

    try:
        # bex 使用bera交换weth
        bera_balance = bera.w3.eth.get_balance(account.address)
        result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, weth_address)
        logger.success(f'bex 使用bera交换weth成功！！！,{result}')
    except Exception as e:
        logger.error(f'bex 使用bera交换weth失败！！！,{e}')

    try:
        # 授权usdc
        approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), usdc_address)
        logger.debug(approve_result)
        # bex 增加 usdc 流动性
        usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
        result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
        logger.debug(result)
        logger.success(f'bex 增加 usdc 流动性成功！！！,{result}')
    except Exception as e:
        logger.error(f'bex 增加 usdc 流动性失败！！！,{e}')

    try:
        # 授权weth
        approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
        logger.debug(approve_result)
        # bex 增加 weth 流动性
        weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
        result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
        logger.success(f'bex 增加 weth 流动性成功！！！,{result}')
    except Exception as e:
        logger.error(f'bex 增加 weth 流动性失败！！！,{e}')

    logger.success('Bex 交互结束')
    logger.debug('-------------------------------------------------------------------------------------')

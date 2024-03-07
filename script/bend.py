from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import bend_address, weth_address, honey_address, bend_pool_address


def bend(account):
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    # 授权
    approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), weth_address)
    logger.debug(approve_result)
    # deposit
    weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
    result = bera.bend_deposit(int(weth_balance), weth_address)
    logger.debug(result)

    # borrow
    balance = bera.bend_contract.functions.getUserAccountData(account.address).call()[2]
    logger.debug(balance)
    result = bera.bend_borrow(int(balance * 0.8 * 1e10), honey_address)
    logger.debug(result)

    # 授权
    approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(approve_result)
    # 查询数量
    call_result = bera.bend_borrows_contract.functions.getUserReservesData(bend_pool_address,
                                                                           bera.account.address).call()
    repay_amount = call_result[0][0][4]
    logger.debug(repay_amount)
    # repay
    result = bera.bend_repay(int(repay_amount * 0.9), honey_address)
    logger.debug(result)

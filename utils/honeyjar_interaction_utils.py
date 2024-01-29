import time

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address, wbear_address


# from config.address_config import bex_swap_address, usdc_address, honey_address, honey_swap_address, \
#     bex_approve_liquidity_address, weth_address, bend_address, bend_borrows_address, wbear_address, zero_address, \
#     ooga_booga_address
def honeyjar_interacte(private_key, rpc_url):
    for _ in range(10):
        if honeyjar_interacte_(private_key, rpc_url):
            return


def honeyjar_interacte_(private_key, rpc_url):
    try:
        logger.debug('0xhoneyjar 交互开始')
        account = Account.from_key(private_key)
        bera = BeraChainTools(private_key=account.key, rpc_url=rpc_url)
        has_mint = bera.ooga_booga_contract.functions.hasMinted(account.address).call()
        if has_mint:
            logger.success(f'之前mint过了,0xhoneyjar 交互成功')
            logger.debug('-------------------------------------------------------------------------------------')
            return True

        # 授权
        approve_result = bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
        honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
        if honey_balance < 42 * 10 ** 17:
            for i in range(10):
                result = bera.bex_swap(int(2 * 10 ** 16), wbear_address, honey_address)
                if result:
                    break
        logger.debug(approve_result)
        # 花费4.2 honey mint
        result = bera.honey_jar_mint()
        # logger.debug(result)
        if result:
            logger.success(f'0xhoneyjar 交互成功,{result}')
            logger.debug('-------------------------------------------------------------------------------------')
            return True
        else:
            return False
    except Exception as e:
        logger.error(f'0xhoneyjar 交互失败，{e}')
        time.sleep(5)
    return False

import time

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address


def honeyjar_interacte(private_key):
    for _ in range(10):
        if honeyjar_interacte_(private_key):
            return


def honeyjar_interacte_(private_key):
    try:
        logger.debug('0xhoneyjar 交互开始')
        account = Account.from_key(private_key)
        bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

        # 授权
        approve_result = bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
        logger.debug(approve_result)
        # 花费4.2 honey mint
        result = bera.honey_jar_mint()
        # logger.debug(result)
        logger.success('0xhoneyjar 交互成功')
        logger.debug('-------------------------------------------------------------------------------------')
        return True
    except Exception as e:
        logger.error(f'0xhoneyjar 交互失败，{e}')
        time.sleep(5)
    return False

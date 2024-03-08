from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address


def honey_jar(account):
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

    # https://faucet.0xhoneyjar.xyz/mint
    # 授权
    approve_result = bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(approve_result)
    bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
    # 花费4.2 honey mint
    result = bera.honey_jar_mint()
    logger.debug(result)

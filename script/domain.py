from loguru import logger

from bera_tools import BeraChainTools


def domain_register(account):
    bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')
    result = bera.create_bera_name()
    logger.debug(result)

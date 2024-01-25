from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from proxy_utils import get_proxy


def generate_wallet(count):
    for _ in range(count):
        try:
            account = Account.create()
            logger.debug(f'address:{account.address}')
            logger.debug(f'key:{account.key.hex()}')
            client_key = '' #填入client_key
            bera = BeraChainTools(private_key=account.key, client_key=client_key, solver_provider='ez-captcha',
                                  rpc_url='https://rpc.ankr.com/berachain_testnet')

            result = bera.claim_bera(proxies=get_proxy())
            logger.debug(result.text)
            with open('../wallet/bera_private_keys.txt', 'a') as f:
                f.write(account.key.hex() + '\n')
        except Exception as e:
            print()


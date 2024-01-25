from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from proxy_utils import get_proxy


def generate_wallet(count):
    for i in range(count):
        try:
            logger.debug(f'生成第{i + 1}个账号')
            account = Account.create()
            logger.debug(f'address:{account.address}')
            logger.debug(f'key:{account.key.hex()}')
            client_key = '' #填入client_key
            bera = BeraChainTools(private_key=account.key, client_key=client_key, solver_provider='ez-captcha',
                                  rpc_url='https://rpc.ankr.com/berachain_testnet')

            result = bera.claim_bera(proxies=get_proxy())
            logger.debug(f'{result.text}\n')
            with open('../wallet/bera_private_keys.txt', 'a') as f:
                f.write(account.key.hex() + '\n')
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    generate_wallet(100)

from eth_account import Account
from loguru import logger
import requests
from bera_tools import BeraChainTools


# from proxy_utils import get_proxy

def get_proxy(proxy_url):
    aaa = requests.get(proxy_url).text
    proxy_host = aaa.splitlines()[0]
    logger.debug('代理IP为：' + proxy_host)
    proxy = {
        'http': 'http://' + proxy_host,
        'https': 'http://' + proxy_host
    }
    return proxy


def generate_wallet(count, rpc_url, proxy_url, solver_provider, client_key, file_path):
    for i in range(count):
        try:
            logger.debug(f'生成第{i + 1}个账号')
            account = Account.create()
            logger.debug(f'address:{account.address}')
            logger.debug(f'key:{account.key.hex()}')
            bera = BeraChainTools(private_key=account.key, client_key=client_key, solver_provider=solver_provider,
                                  rpc_url=rpc_url)
            result = bera.claim_bera(proxies=get_proxy(proxy_url))
            logger.debug(f'{result.text}\n')
            with open(file_path, 'a') as f:
                f.write(account.key.hex() + '\n')
        except Exception as e:
            logger.error(e)

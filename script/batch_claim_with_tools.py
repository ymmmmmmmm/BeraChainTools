import requests
from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools


def claim_with_tools(account):
    logger.debug(f'address:{account.address}')
    logger.debug(f'key:{account.key.hex()}')
    # TODO 填写你的 YesCaptcha client key 或者2Captcha API Key 或者 ez-captcha ClientKey
    client_key = '8457ec6e8961f0e44c0b36443e1155145e4b606536032'
    # 使用yescaptcha solver googlev3
    bera = BeraChainTools(private_key=account.key, client_key=client_key, solver_provider='yescaptcha',
                          rpc_url='https://rpc.ankr.com/berachain_testnet')

    response = requests.get(
            'http://list.rola.vip:8088/user_get_ip_list?token=YKoiKqHxBqM6Fm8b1709609353510&qty=1&country=cl&state=&city=&time=10&format=txt&protocol=http&filter=1')
    proxy_ip = f'http://{response.text.strip()}'

    logger.debug(f'proxy:{proxy_ip}')

    # 使用代理
    result = bera.claim_bera(proxies={'http': proxy_ip, 'https': proxy_ip})
    logger.debug(result.text)

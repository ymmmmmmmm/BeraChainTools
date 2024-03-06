from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools

if __name__ == '__main__':
    account = Account.create()
    logger.debug(f'address:{account.address}')
    logger.debug(f'key:{account.key.hex()}')
    # TODO 填写你的 YesCaptcha client key 或者2Captcha API Key 或者 ez-captcha ClientKey
    client_key = '8457ec6e8961f0e44c0b36443e1155145e4b606536032'
    # 使用yescaptcha solver googlev3
    bera = BeraChainTools(private_key=account.key, client_key=client_key, solver_provider='yescaptcha',
                          rpc_url='https://rpc.ankr.com/berachain_testnet')
    # 使用2captcha solver googlev3
    # bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='2captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
    # 使用ez-captcha solver googlev3
    # bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='ez-captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')

    # 不使用代理
    # result = bera.claim_bera()
    # 使用代理
    proxy = 'http://utoyhnn8:j7xusAXij07hWKLF_country-Singapore@proxy.proxy-cheap.com:31112'
    result = bera.claim_bera(proxies= {'http': proxy, 'https': proxy})
    logger.debug(result.text)
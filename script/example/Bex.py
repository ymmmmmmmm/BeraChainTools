from loguru import logger
from wallet_helper import read_wallets_from_file
from wallet_helper import Wallet
from bera_tools import BeraChainTools
from config.address_config import (
    usdc_address, wbear_address, weth_address, bex_swap_address, bex_approve_liquidity_address,
    usdc_pool_liquidity_address, weth_pool_liquidity_address
)
from loguru import logger

from wallet_helper import Wallet
from wallet_helper import read_wallets_from_file
from bera_tools import BeraChainTools
from config.address_config import (
    usdc_address, wbear_address, weth_address, bex_swap_address, bex_approve_liquidity_address,
    usdc_pool_liquidity_address, weth_pool_liquidity_address
)


def do_transactions(wallet: Wallet):
    logger.debug(f'key -> {wallet.private_key} \n address -> {wallet.address}')
    bera = BeraChainTools(private_key=wallet.private_key, solver_provider='yescaptcha',
                          rpc_url='https://rpc.ankr.com/berachain_testnet')

    approve_result = bera.approve_token(bex_swap_address, int("0x" + "f" * 64, 16), usdc_address)
    # bex 使用bera交换usdc
    bera_balance = bera.w3.eth.get_balance(wallet.address)
    logger.debug(f'balance -> {bera_balance}')
    result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, usdc_address)
    logger.debug(f'bera -> usdc {result}')

    # bex 使用usdc交换weth
    usdc_balance = bera.usdc_contract.functions.balanceOf(wallet.address).call()
    result = bera.bex_swap(int(usdc_balance * 0.2), usdc_address, weth_address)
    logger.debug(f'usdc -> weth {result}')

    # 授权usdc
    approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), usdc_address)
    logger.debug(approve_result)
    # bex 增加 usdc 流动性
    usdc_balance = bera.usdc_contract.functions.balanceOf(wallet.address).call()
    result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
    logger.debug(result)

    # 授权weth
    approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
    logger.debug(approve_result)
    # bex 增加 weth 流动性
    weth_balance = bera.weth_contract.functions.balanceOf(wallet.address).call()
    result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
    logger.debug(result)


if __name__ == '__main__':
    filename = './account/accounts.txt'
    wallets = read_wallets_from_file(filename)
    for wallet in wallets:
        do_transactions(wallet)

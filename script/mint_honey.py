from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import honey_swap_address, usdc_address, honey_address


def mint_honey(account):
    bera = BeraChainTools(private_key=account.key, solver_provider='yescaptcha',
                          rpc_url='https://rpc.ankr.com/berachain_testnet')
    # 授权usdc
    approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
    logger.debug(f'approve usdc -> {approve_result}')
    # 使用usdc mint honey
    usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
    mint_result = bera.honey_mint(int(usdc_balance * 0.5))
    logger.debug(f'mint honey with usdc -> {mint_result}')

    # 授权honey
    approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
    logger.debug(f'approve honey -> {approve_result}')
    # 赎回
    honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
    redeem_result = bera.honey_redeem(int(honey_balance * 0.5))
    logger.debug(f'honey_redeem honey -> {redeem_result}')

# -*- coding: utf-8 -*-
# Time     :2024/1/22 01:21
# Author   :ym
# File     :example.py

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import honey_address, bend_pool_address

# 创建钱包
account = Account.create()
# account = Account.from_key('')
logger.debug(f'address:{account.address}')
logger.debug(f'key:{account.key.hex()}')

# TODO 填写你的 client key
yes_captcha_client_key = ''
# bera = BeraChainTools(private_key=account.key, client_key=yes_captcha_client_key,solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
bera = BeraChainTools(private_key=account.key, client_key=yes_captcha_client_key, solver_provider='2captcha',
                      rpc_url='https://rpc.ankr.com/berachain_testnet')

# 领水
# result = bera.claim_bera()
# logger.debug(result.text)
# bex 使用bera交换usdc
# bera_balance = bera.w3.eth.get_balance(account.address)
# result = bera.bex_swap(int(bera_balance * 0.2), usdc_pool_address, usdc_address)
# logger.debug(result)
# # bex 使用bera交换weth
# bera_balance = bera.w3.eth.get_balance(account.address)
# result = bera.bex_swap(int(bera_balance * 0.3), weth_pool_address, weth_address)
# logger.debug(result)
# # 授权usdc
# approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), usdc_address)
# logger.debug(approve_result)
#
# # bex 增加 usdc 流动性
# usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
# result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
# logger.debug(result)
# # 授权weth
# approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
# logger.debug(approve_result)
#
# # bex 增加 weth 流动性
# weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
# result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
# logger.debug(result)
# # honey mint
#
# approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
# logger.debug(approve_result)
#
# usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
# result = bera.honey_mint(int(usdc_balance * 0.5))
# logger.debug(result)
# # #  honey redeem
# approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
# logger.debug(approve_result)
# honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
# result = bera.honey_redeem(int(honey_balance * 0.5))
# logger.debug(result)
#
# # # bend eposit
# weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
# result = bera.bend_deposit(int(weth_balance), weth_address)
# logger.debug(result)

# bend borrow
# balance = bera.bend_contract.functions.getUserAccountData(account.address).call()[2]
# logger.debug(balance)
# result = bera.bend_borrow(int(balance*0.8*1e10),honey_address)
# logger.debug(result)

# bend repay
# approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), honey_address)
# logger.debug(approve_result)
call_result = bera.bend_borrows_contract.functions.getUserReservesData(bend_pool_address, bera.account.address).call()
repay_amount = call_result[0][0][4]
logger.debug(repay_amount)
result = bera.bend_repay(int(repay_amount * 0.9), honey_address)
logger.debug(result)

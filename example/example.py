# -*- coding: utf-8 -*-
# Time     :2024/1/22 01:21
# Author   :ym
# File     :example.py
import time

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import weth_address, weth_pool_address, usdc_pool_address, usdc_address, \
    weth_pool_liquidity_address, bex_approve_liquidity_address, honey_swap_address, honey_address, \
    usdc_pool_liquidity_address

# 创建钱包
# account = Account.create()
account = Account.from_key('1b79aa2f9f75758b6046a8edcee48b82574217547ba4333ef94769237110229b')
logger.debug(f'address:{account.address}')
logger.debug(f'key:{account.key.hex()}')

# TODO 填写你的 client key
yes_captcha_client_key = 'xxxxxxxxx'
bera = BeraChainTools(private_key=account.key, yes_captcha_client_key=yes_captcha_client_key,
                      rpc_url='https://rpc.ankr.com/berachain_testnet')

# 领水
result = bera.claim_bera()
logger.debug(result.text)
time.sleep(5)
# bex 使用bera交换usdc
bera_balance = bera.w3.eth.get_balance(account.address)
result = bera.bex_swap(int(bera_balance * 0.2), usdc_pool_address, usdc_address)
logger.debug(result)
# bex 使用bera交换weth
bera_balance = bera.w3.eth.get_balance(account.address)
result = bera.bex_swap(int(bera_balance * 0.3), weth_pool_address, weth_address)
logger.debug(result)
# 授权usdc
approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), usdc_address)
logger.debug(approve_result)

# bex 增加 usdc 流动性
usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
result = bera.bex_add_liquidity(int(usdc_balance * 0.5), usdc_pool_liquidity_address, usdc_address)
logger.debug(result)
# 授权weth
approve_result = bera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), weth_address)
logger.debug(approve_result)

# bex 增加 weth 流动性
weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
result = bera.bex_add_liquidity(int(weth_balance * 0.5), weth_pool_liquidity_address, weth_address)
logger.debug(result)
# honey mint

approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
logger.debug(approve_result)

usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
result = bera.honey_mint(int(usdc_balance * 0.5))
logger.debug(result)
# #  honey redeem
approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
logger.debug(approve_result)
honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
result = bera.honey_redeem(int(honey_balance * 0.5))
logger.debug(result)

# # bend eposit
weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
result = bera.bend_deposit(int(weth_balance), weth_address)
logger.debug(result)

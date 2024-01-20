# -*- coding: utf-8 -*-
# Time     :2024/1/21 00:09
# Author   :ym
# File     :bex_swap.py
import random
from typing import Union

from eth_account import Account
from eth_typing import Address, ChecksumAddress, HexStr
from loguru import logger
from web3 import Web3

from config.abi_config import bex_abi, erc_20_abi
from config.address_config import bex_swap_address, zero_address, weth_address, weth_pool_address, usdc_address, \
    usdc_pool_liquidity_address, bex_approve_liquidity_address, usdc_pool_address

w3 = Web3(Web3.HTTPProvider('https://artio.rpc.berachain.com/'))
bex_contract = w3.eth.contract(address=bex_swap_address, abi=bex_abi)


@logger.catch
def bex_swap(address: Union[Address, ChecksumAddress], private_key: Union[bytes, HexStr, int],
             pool_address: Union[Address], asset_out_address: Union[Address, ChecksumAddress]) -> str:
    """
    bex 交换代币
    :param address: 需要交互的钱包地址
    :param private_key: 需要交互的钱包私钥
    :param pool_address: 交互的pool id
    :param asset_out_address: 输出的token合约地址
    :return: hash
    """
    balance = w3.eth.get_balance(address)
    logger.debug(balance)
    assert balance != 0
    # 支付BERA占比
    nonce = w3.eth.get_transaction_count(address)
    value = int(balance * 0.1)
    txn = bex_contract.functions.batchSwap(kind=0, swaps=[
        dict(poolId=pool_address, assetIn=zero_address, amountIn=value, assetOut=asset_out_address, amountOut=0,
             userData=b'')], deadline=99999999).build_transaction(
        {'gas': 300000 + random.randint(1, 10000), 'value': value, 'gasPrice': int(w3.eth.gas_price * 1.1),
         'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    order_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.debug(f'{address}:{order_hash.hex()}')
    order_result = w3.eth.wait_for_transaction_receipt(order_hash, timeout=360)
    if order_result.status == 1:
        logger.success(f'{address}:{order_hash.hex()}')
    else:
        logger.critical(f'{address}:{order_hash.hex()}')
        raise ValueError(f'{address}:{order_hash.hex()}')
    return order_hash.hex()


@logger.catch
def bex_add_liquidity(address: Union[Address, ChecksumAddress], private_key: Union[bytes, HexStr, int],
                      pool_address: Union[Address], asset_in_address: Union[Address]) -> str:
    """
    加流动性
    :param address: 需要交互的钱包地址
    :param private_key: 需要交互的钱包私钥
    :param pool_address: 需要加流动性的pool地址
    :param asset_in_address: 需要加流动性的token地址
    :return: hash
    """
    asset_in_token_contract = w3.eth.contract(address=asset_in_address, abi=erc_20_abi)
    token_balance = asset_in_token_contract.functions.balanceOf(address).call()
    assert token_balance != 0
    # 支付 token 占比
    value = int(token_balance * 0.8)
    allowance_balance = asset_in_token_contract.functions.allowance(address, bex_approve_liquidity_address).call()
    nonce = w3.eth.get_transaction_count(address)
    if allowance_balance < value:
        # 需要授权
        txn = w3.eth.account.sign_transaction(dict(
            nonce=nonce,
            chainId=80085,
            gasPrice=int(w3.eth.gas_price * 1.15),
            gas=50000 + random.randint(1, 10000),
            to=asset_in_address,
            data='0x095ea7b300000000000000000000000000000000000000000000000000000000006969697fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
        ), private_key)
        order_hash = w3.eth.send_raw_transaction(txn.rawTransaction)
        logger.debug(f'{address}:{order_hash.hex()}')
        order_result = w3.eth.wait_for_transaction_receipt(order_hash, timeout=360)
        if order_result.status == 1:
            logger.success(f'{address}:{order_hash.hex()}')
        else:
            logger.critical(f'{address}:{order_hash.hex()}')
            raise ValueError(f'{address}:{order_hash.hex()}')
        nonce += 1
    txn = bex_contract.functions.addLiquidity(pool=pool_address, receiver=address, assetsIn=[asset_in_address],
                                              amountsIn=[value]).build_transaction(
        {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(w3.eth.gas_price * 1.1),
         'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    order_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.debug(f'{address}:{order_hash.hex()}')
    order_result = w3.eth.wait_for_transaction_receipt(order_hash, timeout=360)
    if order_result.status == 1:
        logger.success(f'{address}:{order_hash.hex()}')
    else:
        logger.critical(f'{address}:{order_hash.hex()}')
        raise ValueError(f'{address}:{order_hash.hex()}')
    return order_hash.hex()


def run(key):
    account = Account.from_key(key)
    bex_swap(account.address, account.key, usdc_pool_address, usdc_address)
    bex_swap(account.address, account.key, weth_pool_address, weth_address)
    bex_add_liquidity(account.address, account.key, usdc_pool_liquidity_address, usdc_address)


def test_run():
    account = Account.create()
    # 使用bera交换usc
    bex_swap(account.address, account.key, usdc_pool_address, usdc_address)
    # 使用bera交换weth
    bex_swap(account.address, account.key, weth_pool_address, weth_address)
    # 添加usdc流动性
    bex_add_liquidity(account.address, account.key, usdc_pool_liquidity_address, usdc_address)


if __name__ == '__main__':
    # 读取当前文件夹下面的bera_claim_success(领取成功文本)
    with open('./bera_claim_success.txt', 'r') as f:
        wallet_list = f.readlines()
    for _ in wallet_list:
        _key = _.split('----')[1].replace('\n', '')
        run(_key)

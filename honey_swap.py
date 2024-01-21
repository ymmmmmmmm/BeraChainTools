# -*- coding: utf-8 -*-
# Time     :2024/1/21 11:36
# Author   :ym
# File     :honey_swap.py
import concurrent.futures
import os
import random
import time
from typing import Union

from dotenv import load_dotenv
from eth_account import Account
from eth_typing import Address, ChecksumAddress, HexStr
from loguru import logger
from web3 import Web3

from config.address_config import honey_swap_address, usdc_address, honey_address
from config.contract_config import usdc_contract, honey_swap_contract, honey_contract

load_dotenv()
max_workers = int(os.getenv("MaxWorkers"))
rpc_url = os.getenv("RPC_URL")
w3 = Web3(Web3.HTTPProvider(rpc_url))


@logger.catch
def honey_mint(address: Union[Address, ChecksumAddress], private_key: Union[bytes, HexStr, int]) -> str:
    usdc_balance = usdc_contract.functions.balanceOf(address).call()
    assert usdc_balance != 0
    # 支付 usdc 占比
    value = int(usdc_balance * 0.8)
    allowance_balance = usdc_contract.functions.allowance(address, honey_swap_address).call()
    nonce = w3.eth.get_transaction_count(address)
    if allowance_balance < value:
        # 需要授权
        txn = w3.eth.account.sign_transaction(dict(
            nonce=nonce,
            chainId=80085,
            gasPrice=int(w3.eth.gas_price * 1.15),
            gas=50000 + random.randint(1, 10000),
            to=usdc_address,
            data='0x095ea7b300000000000000000000000009ec711b81cd27a6466ec40960f2f8d85bb129d97fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
        ), private_key)
        order_hash = w3.eth.send_raw_transaction(txn.rawTransaction)
        logger.debug(f'{address}:{order_hash.hex()}')
        order_result = w3.eth.wait_for_transaction_receipt(order_hash, timeout=120)
        if order_result.status == 1:
            logger.success(f'{address}:{order_hash.hex()}')
        else:
            logger.critical(f'{address}:{order_hash.hex()}')
            raise ValueError(f'{address}:{order_hash.hex()}')
        nonce += 1
    txn = honey_swap_contract.functions.mint(to=address, collateral=usdc_address, amount=value, ).build_transaction(
        {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(w3.eth.gas_price * 1.15), 'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    order_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.debug(f'{address}:{order_hash.hex()}')
    order_result = w3.eth.wait_for_transaction_receipt(order_hash, timeout=120)
    if order_result.status == 1:
        logger.success(f'{address}:{order_hash.hex()}')
    else:
        logger.critical(f'{address}:{order_hash.hex()}')
        raise ValueError(f'{address}:{order_hash.hex()}')
    return order_hash.hex()


@logger.catch
def honey_redeem(address: Union[Address, ChecksumAddress], private_key: Union[bytes, HexStr, int]) -> str:
    honey_balance = honey_contract.functions.balanceOf(address).call()
    assert honey_balance != 0
    # 支付 honey 占比
    value = int(honey_balance * 0.8)
    allowance_balance = honey_contract.functions.allowance(address, honey_swap_address).call()
    logger.debug(allowance_balance)
    nonce = w3.eth.get_transaction_count(address)
    if allowance_balance < value:
        # 需要授权
        txn = w3.eth.account.sign_transaction(dict(
            nonce=nonce,
            chainId=80085,
            gasPrice=int(w3.eth.gas_price * 1.15),
            gas=50000 + random.randint(1, 10000),
            to=honey_address,
            data='0x095ea7b300000000000000000000000009ec711b81cd27a6466ec40960f2f8d85bb129d97fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff',
        ), private_key)
        order_hash = w3.eth.send_raw_transaction(txn.rawTransaction)
        logger.debug(f'{address}:{order_hash.hex()}')
        order_result = w3.eth.wait_for_transaction_receipt(order_hash, timeout=120)
        if order_result.status == 1:
            logger.success(f'{address}:{order_hash.hex()}')
        else:
            logger.critical(f'{address}:{order_hash.hex()}')
            raise ValueError(f'{address}:{order_hash.hex()}')
        nonce += 1
    txn = honey_swap_contract.functions.redeem(to=address, amount=value, collateral=usdc_address).build_transaction(
        {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(w3.eth.gas_price * 1.15), 'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    order_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    logger.debug(f'{address}:{order_hash.hex()}')
    order_result = w3.eth.wait_for_transaction_receipt(order_hash, timeout=120)
    if order_result.status == 1:
        logger.success(f'{address}:{order_hash.hex()}')
    else:
        logger.critical(f'{address}:{order_hash.hex()}')
        raise ValueError(f'{address}:{order_hash.hex()}')
    return order_hash.hex()


def honey_run(key):
    account = Account.from_key(key)
    honey_mint(account.address, account.key)
    time.sleep(random.randint(5, 20))
    honey_redeem(account.address, account.key)


def ym_test_run():
    account = Account.create()
    # mint 操作 usdc换honey
    honey_mint(account.address, account.key)
    # redeem 操作 honey换usdc
    honey_redeem(account.address, account.key)


if __name__ == '__main__':
    # 读取当前文件夹下面的bera_claim_success(领取成功文本)
    with open('./bera_claim_success.txt', 'r') as f:
        wallet_list = f.readlines()
    random.shuffle(wallet_list)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(honey_run, i.split('----')[1].replace('\n', '')) for i in wallet_list]

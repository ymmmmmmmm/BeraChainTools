import asyncio
import concurrent.futures
import random
import threading

from eth_account import Account
from loguru import logger
from web3 import Web3

from script.batch_bex import batch_swap
from script.bend import bend
from script.contract_deployment import deployment
from script.domain import domain_register
from script.example.wallet_helper import read_wallets_from_file, list_balance, record_address
from script.honey_jar import honey_jar
from script.mint_honey import mint_honey


def balance_of(address):
    w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/berachain_testnet'))
    balance_wei = w3.eth.get_balance(address)
    return w3.from_wei(balance_wei, 'ether')


def batch_run(wallets):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(handle_wallet, wallet) for wallet in wallets]

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            # 获取每个任务的结果，即便我们这里不需要结果
            pass


def handle_wallet(wallet):
    try:
        account = Account.from_key(wallet.private_key)
        bera_balance = balance_of(account.address)
        logger.info(f'balance -> {bera_balance}')
        logger.info(f'task - {threading.currentThread().getName()}, start \n address: {account.address}')
        logger.info(f'{account.address} | start swap ')
        batch_swap(account)
        logger.info(f'{account.address} | start mint ')
        mint_honey(account)
        logger.info(f'{account.address} | start bend ')
        bend(account)
        logger.info(f'{account.address} | start honey_jar ')
        honey_jar(account)
        logger.info(f'{account.address} | start deployment_contract ')
        deployment(account)
        logger.info(f'{account.address} | start register_domain ')
        domain_register(account)
    except Exception as e:
        json = e.__str__()
        logger.error(json)


def single_run(wallet):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(handle_wallet, wallet)


async def _list_balance(balance_record):
    for record in balance_record:
        await list_balance('./balance/balance_record.txt', record[0], record[1])


if __name__ == '__main__':
    # claim_with_tools()
    # 1. load wallets
    wallets = read_wallets_from_file('./example/account/accounts.txt')
    valid_wallet = None
    balance_record = []
    for wallet in wallets:
        account = Account.from_key(wallet.private_key)
        balance = balance_of(account.address)
        limit = random.uniform(0.1, 0.2)
        logger.info(f'limit balance: {limit}')
        # record empty
        if balance == 0:
            asyncio.run(record_address('./zero_balance/zero_balance.txt', account.address))
        elif balance >= limit:
            single_run(wallet)
        logger.info(f'address : {account.address}, balance : {balance}')
        balance_record.append([account.address, balance])

    asyncio.run(_list_balance(balance_record))

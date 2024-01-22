# -*- coding: utf-8 -*-
# Time     :2024/1/22 00:36
# Author   :ym
# File     :bera_tools.py
import json
import random
import time
from typing import Union

import requests
from eth_account import Account
from eth_typing import Address, ChecksumAddress
from faker import Faker
from requests import Response
from web3 import Web3

from config.abi_config import erc_20_abi, honey_abi, bex_abi, bend_abi
from config.address_config import bex_swap_address, usdc_address, honey_address, honey_swap_address, zero_address, \
    bex_approve_liquidity_address, weth_address, bend_address


class BeraChainTools(object):
    def __init__(self, private_key, client_key='', solver_provider='', rpc_url='https://artio.rpc.berachain.com/'):
        if solver_provider not in ["yescaptcha", "2captcha", ""]:
            raise ValueError("solver_provider must be 'yescaptcha' or '2captcha'")
        self.solver_provider = solver_provider
        self.private_key = private_key
        self.client_key = client_key
        self.rpc_url = rpc_url
        self.fake = Faker()
        self.account = Account.from_key(self.private_key)
        self.session = requests.session()
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.bex_contract = self.w3.eth.contract(address=bex_swap_address, abi=bex_abi)
        self.honey_swap_contract = self.w3.eth.contract(address=honey_swap_address, abi=honey_abi)
        self.usdc_contract = self.w3.eth.contract(address=usdc_address, abi=erc_20_abi)
        self.weth_contract = self.w3.eth.contract(address=weth_address, abi=erc_20_abi)
        self.honey_contract = self.w3.eth.contract(address=honey_address, abi=erc_20_abi)
        self.bend_contract = self.w3.eth.contract(address=bend_address, abi=bend_abi)

    def get_2captcha_google_token(self) -> Union[bool, str]:
        if self.client_key == '':
            raise ValueError('2captcha_client_key is null ')
        params = {'key': self.client_key, 'method': 'userrecaptcha', 'version': 'v3', 'action': 'submit',
                  'min_score': 0.5,
                  'googlekey': '6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH',
                  'pageurl': 'https://artio.faucet.berachain.com/',
                  'json': 1}
        response = requests.get(f'https://2captcha.com/in.php?', params=params).json()
        if response['status'] != 1:
            raise ValueError(response)
        task_id = response['request']
        for _ in range(60):
            response = requests.get(
                f'https://2captcha.com/res.php?key={self.client_key}&action=get&id={task_id}&json=1').json()
            if response['status'] == 1:
                return response['request']
            else:
                time.sleep(3)
        return False

    def get_yescaptcha_google_token(self) -> Union[bool, str]:
        if self.client_key == '':
            raise ValueError('yes_captcha_client_key is null ')
        json_data = {"clientKey": self.client_key,
                     "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                              "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                              "type": "RecaptchaV3TaskProxylessM1S7", "pageAction": "submit"}, "softID": 109}
        response = self.session.post(url='https://api.yescaptcha.com/createTask', json=json_data).json()
        if response['errorId'] != 0:
            raise ValueError(response)
        task_id = response['taskId']
        time.sleep(5)
        for _ in range(30):
            data = {"clientKey": self.client_key, "taskId": task_id}
            response = requests.post(url='https://api.yescaptcha.com/getTaskResult', json=data).json()
            if response['status'] == 'ready':
                return response['solution']['gRecaptchaResponse']
            else:
                time.sleep(2)
        return False

    def get_nonce(self):
        return self.w3.eth.get_transaction_count(self.account.address)

    def claim_bera(self, proxies=None) -> Response:
        """
        bera领水
        :param proxies: http代理
        :return: object
        """
        if self.solver_provider == 'yescaptcha':
            google_token = self.get_yescaptcha_google_token()
        elif self.solver_provider == '2captcha':
            google_token = self.get_2captcha_google_token()
        else:
            raise ValueError("solver_provider must be 'yescaptcha' or '2captcha'")
        if not google_token:
            raise ValueError('获取google token 出错')
        user_agent = self.fake.chrome()
        headers = {'authority': 'artio-80085-ts-faucet-api-2.berachain.com', 'accept': '*/*',
                   'accept-language': 'zh-CN,zh;q=0.9', 'authorization': f'Bearer {google_token}',
                   'cache-control': 'no-cache', 'content-type': 'text/plain;charset=UTF-8',
                   'origin': 'https://artio.faucet.berachain.com', 'pragma': 'no-cache',
                   'referer': 'https://artio.faucet.berachain.com/', 'user-agent': user_agent}
        params = {'address': self.account.address}
        if proxies is not None:
            proxies = {"http": f"http://{proxies}", "https": f"http://{proxies}"}
        response = requests.post('https://artio-80085-ts-faucet-api-2.berachain.com/api/claim', params=params,
                                 headers=headers, data=json.dumps(params), proxies=proxies)
        return response

    def approve_token(self, spender: Union[Address, ChecksumAddress], amount: int,
                      approve_token_address: Union[Address, ChecksumAddress]) -> str:
        """
        授权代币
        :param spender: 授权给哪个地址
        :param amount: 授权金额
        :param approve_token_address: 需要授权的代币地址
        :return: hash
        """
        approve_contract = self.w3.eth.contract(address=approve_token_address, abi=erc_20_abi)
        txn = approve_contract.functions.approve(spender, amount).build_transaction(
            {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def bex_swap(self, amount_in: int, pool_address: Union[Address],
                 asset_out_address: Union[Address, ChecksumAddress]) -> str:
        """
        bex交换代币
        :param amount_in: 加流动性的数量
        :param pool_address: 交互的pool 地址
        :param asset_out_address: 输出的token合约地址
        :return:
        """

        balance = self.w3.eth.get_balance(self.account.address)
        assert balance != 0
        assert balance >= amount_in
        # 支付BERA占比
        txn = self.bex_contract.functions.batchSwap(kind=0, swaps=[
            dict(poolId=pool_address, assetIn=zero_address, amountIn=amount_in, assetOut=asset_out_address, amountOut=0,
                 userData=b'')], deadline=99999999).build_transaction(
            {'gas': 300000 + random.randint(1, 10000), 'value': amount_in,
             'gasPrice': int(self.w3.eth.gas_price * 1.2),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def bex_add_liquidity(self, amount_in: int, pool_address: Union[Address], asset_in_address: Union[Address]) -> str:
        """
        bex 增加流动性
        :param amount_in: 输入数量
        :param pool_address: 交互的pool 地址
        :param asset_in_address: 需要加流动性的token地址
        :return:
        """
        asset_in_token_contract = self.w3.eth.contract(address=asset_in_address, abi=erc_20_abi)
        token_balance = asset_in_token_contract.functions.balanceOf(self.account.address).call()
        assert token_balance != 0
        assert token_balance >= amount_in
        allowance_balance = asset_in_token_contract.functions.allowance(self.account.address,
                                                                        bex_approve_liquidity_address).call()
        if allowance_balance < amount_in:
            raise ValueError('需要授权')
        txn = self.bex_contract.functions.addLiquidity(pool=pool_address, receiver=self.account.address,
                                                       assetsIn=[asset_in_address],
                                                       amountsIn=[amount_in]).build_transaction(
            {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def honey_mint(self, amount_usdc_in: int):
        """
        honey mint
        :param amount_usdc_in: 输入数量
        :return:
        """
        usdc_balance = self.usdc_contract.functions.balanceOf(self.account.address).call()
        assert usdc_balance != 0
        assert usdc_balance >= amount_usdc_in
        allowance_balance = self.usdc_contract.functions.allowance(self.account.address, honey_swap_address).call()
        if allowance_balance < amount_usdc_in:
            raise ValueError('需要授权')
        txn = self.honey_swap_contract.functions.mint(to=self.account.address, collateral=usdc_address,
                                                      amount=amount_usdc_in, ).build_transaction(
            {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def honey_redeem(self, amount_honey_in) -> str:
        """
        honey redeem
        :param amount_honey_in: 输入数量
        :return:
        """
        honey_balance = self.honey_contract.functions.balanceOf(self.account.address).call()
        assert honey_balance != 0
        assert honey_balance >= amount_honey_in
        allowance_balance = self.honey_contract.functions.allowance(self.account.address, honey_swap_address).call()
        if allowance_balance < amount_honey_in:
            raise ValueError('需要授权')

        txn = self.honey_swap_contract.functions.redeem(to=self.account.address, amount=amount_honey_in,
                                                        collateral=usdc_address).build_transaction(
            {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def bend_deposit(self, amount_in, amount_in_token_address):
        amount_in_token_contract = self.w3.eth.contract(address=amount_in_token_address, abi=erc_20_abi)
        token_balance = amount_in_token_contract.functions.balanceOf(self.account.address).call()
        assert token_balance != 0
        assert token_balance >= amount_in
        allowance_balance = amount_in_token_contract.functions.allowance(self.account.address,
                                                                         bend_address).call()
        if allowance_balance < amount_in:
            raise ValueError('需要授权')
        txn = self.bend_contract.functions.supply(asset=amount_in_token_address, amount=amount_in,
                                                  onBehalfOf=self.account.address, referralCode=0).build_transaction(
            {'gas': 300000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

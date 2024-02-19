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
from solcx import compile_source, set_solc_version
from web3 import Web3

from config.abi_config import erc_20_abi, honey_abi, bex_abi, bend_abi, bend_borrows_abi, ooga_booga_abi, bera_name_abi
from config.address_config import bex_swap_address, usdc_address, honey_address, honey_swap_address, \
    bex_approve_liquidity_address, weth_address, bend_address, bend_borrows_address, wbear_address, zero_address, \
    ooga_booga_address, bera_name_address
from config.other_config import emoji_list


class BeraChainTools(object):
    def __init__(self, private_key, client_key='', solver_provider='', rpc_url='https://artio.rpc.berachain.com/'):
        # if solver_provider not in ["yescaptcha", "2captcha", "ez-captcha", ""]:
        if solver_provider not in ["yescaptcha", "2captcha"]:
            raise ValueError("solver_provider must be 'yescaptcha' or '2captcha' or 'ez-captcha' ")
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
        self.bend_borrows_contract = self.w3.eth.contract(address=bend_borrows_address, abi=bend_borrows_abi)
        self.ooga_booga_contract = self.w3.eth.contract(address=ooga_booga_address, abi=ooga_booga_abi)
        self.bera_name_contract = self.w3.eth.contract(address=bera_name_address, abi=bera_name_abi)

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

    def get_2captcha_turnstile_token(self) -> Union[bool, str]:
        if self.client_key == '':
            raise ValueError('2captcha_client_key is null ')
        params = {'key': self.client_key, 'method': 'turnstile',
                  'sitekey': '0x4AAAAAAARdAuciFArKhVwt',
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

    def get_yescaptcha_turnstile_token(self) -> Union[bool, str]:
        if self.client_key == '':
            raise ValueError('yes_captcha_client_key is null ')
        json_data = {"clientKey": self.client_key,
                     "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                              "websiteKey": "0x4AAAAAAARdAuciFArKhVwt",
                              "type": "TurnstileTaskProxylessM1"}, "softID": 109}
        response = self.session.post(url='https://api.yescaptcha.com/createTask', json=json_data).json()
        if response['errorId'] != 0:
            raise ValueError(response)
        task_id = response['taskId']
        time.sleep(5)
        for _ in range(30):
            data = {"clientKey": self.client_key, "taskId": task_id}
            response = requests.post(url='https://api.yescaptcha.com/getTaskResult', json=data).json()
            if response['status'] == 'ready':
                return response['solution']['token']
            else:
                time.sleep(2)
        return False

    def get_ez_captcha_google_token(self) -> Union[bool, str]:
        if self.client_key == '':
            raise ValueError('ez-captcha is null ')
        json_data = {
            "clientKey": self.client_key,
            "task": {"websiteURL": "https://artio.faucet.berachain.com/",
                     "websiteKey": "6LfOA04pAAAAAL9ttkwIz40hC63_7IsaU2MgcwVH",
                     "type": "ReCaptchaV3TaskProxyless", }, 'appId': '34119'}
        response = self.session.post(url='https://api.ez-captcha.com/createTask', json=json_data).json()
        if response['errorId'] != 0:
            raise ValueError(response)
        task_id = response['taskId']
        time.sleep(5)
        for _ in range(30):
            data = {"clientKey": self.client_key, "taskId": task_id}
            response = requests.post(url='https://api.ez-captcha.com/getTaskResult', json=data).json()
            if response['status'] == 'ready':
                return response['solution']['gRecaptchaResponse']
            else:
                time.sleep(2)
        return False

    def get_nonce(self):
        return self.w3.eth.get_transaction_count(self.account.address)

    def get_solver_provider(self):
        provider_dict = {
            # 'yescaptcha': self.get_yescaptcha_google_token,
            'yescaptcha': self.get_yescaptcha_turnstile_token,
            '2captcha': self.get_2captcha_turnstile_token,
            'ez-captcha': self.get_ez_captcha_google_token,
        }
        if self.solver_provider not in list(provider_dict.keys()):
            raise ValueError("solver_provider must be 'yescaptcha' or '2captcha' or 'ez-captcha' ")
        return provider_dict[self.solver_provider]()

    def claim_bera(self, proxies=None) -> Response:
        """
        bera领水
        :param proxies: http代理
        :return: object
        """
        google_token = self.get_solver_provider()
        if not google_token:
            raise ValueError('获取google token 出错')
        user_agent = self.fake.chrome()
        headers = {'authority': 'artio-80085-ts-faucet-api-2.berachain.com', 'accept': '*/*',
                   'accept-language': 'zh-CN,zh;q=0.9', 'authorization': f'Bearer {google_token}',
                   'cache-control': 'no-cache', 'content-type': 'text/plain;charset=UTF-8',
                   'origin': 'https://artio.faucet.berachain.com', 'pragma': 'no-cache',
                   'referer': 'https://artio.faucet.berachain.com/', 'user-agent': user_agent}
        # print(headers)
        params = {'address': self.account.address}
        # if proxies is not None:
        #     proxies = {"http": f"http://{proxies}", "https": f"http://{proxies}"}
        response = requests.post('https://artio-80085-faucet-api-cf.berachain.com/api/claim', params=params,
                                 headers=headers, data=json.dumps(params), proxies=proxies)
        return response

    def approve_token(self, spender: Union[Address, ChecksumAddress], amount: int,
                      approve_token_address: Union[Address, ChecksumAddress]) -> Union[bool, str]:
        """
        授权代币
        :param spender: 授权给哪个地址
        :param amount: 授权金额
        :param approve_token_address: 需要授权的代币地址
        :return: hash
        """
        approve_contract = self.w3.eth.contract(address=approve_token_address, abi=erc_20_abi)

        allowance_balance = approve_contract.functions.allowance(self.account.address, spender).call()
        if allowance_balance < amount:
            txn = approve_contract.functions.approve(spender, amount).build_transaction(
                {'gas': 500000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
                 'nonce': self.get_nonce()})
            signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
            order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            return order_hash.hex()
        return True

    def bex_swap(self, amount_in: int, asset_in_address: Union[Address, ChecksumAddress],
                 asset_out_address: Union[Address, ChecksumAddress]) -> str:
        """
        bex 交换
        :param amount_in: 输入数量
        :param asset_in_address: 输入 token 地址
        :param asset_out_address: 输出 token 地址
        :return:
        """
        if asset_in_address == wbear_address:
            balance = self.w3.eth.get_balance(self.account.address)
            assert balance != 0
            assert balance >= amount_in
        else:
            asset_in_token_contract = self.w3.eth.contract(address=asset_in_address, abi=erc_20_abi)
            balance = asset_in_token_contract.functions.balanceOf(self.account.address).call()
            assert balance != 0
            assert balance >= amount_in
            allowance_balance = asset_in_token_contract.functions.allowance(self.account.address,
                                                                            bex_swap_address).call()
            if allowance_balance < amount_in:
                raise ValueError(
                    f'需要授权\nplease run : \nbera.approve_token(bex_swap_address, int("0x" + "f" * 64, 16), "{asset_in_address}")')

        headers = {'authority': 'artio-80085-dex-router.berachain.com', 'accept': '*/*',
                   'accept-language': 'zh-CN,zh;q=0.9', 'cache-control': 'no-cache',
                   'origin': 'https://artio.bex.berachain.com', 'pragma': 'no-cache',
                   'referer': 'https://artio.bex.berachain.com/', 'user-agent': self.fake.chrome()}

        params = {'quoteAsset': asset_out_address, 'baseAsset': asset_in_address, 'amount': amount_in,
                  'swap_type': 'given_in'}

        response = self.session.get('https://artio-80085-dex-router.berachain.com/dex/route', params=params,
                                    headers=headers)
        assert response.status_code == 200
        swaps_list = response.json()['steps']
        swaps = list()
        for index, info in enumerate(swaps_list):
            swaps.append(dict(
                poolId=self.w3.to_checksum_address(info['pool']),
                assetIn=self.w3.to_checksum_address(info['assetIn']),
                amountIn=int(info['amountIn']),
                assetOut=self.w3.to_checksum_address(info['assetOut']),
                amountOut=0 if index + 1 != len(swaps_list) else int(int(info['amountOut']) * 0.5),
                userData=b''))
        if asset_in_address.lower() == wbear_address.lower():
            swaps[0]['assetIn'] = zero_address

        txn = self.bex_contract.functions.batchSwap(kind=0, swaps=swaps, deadline=99999999).build_transaction(
            {'gas': 500000 + random.randint(1, 10000), 'value': amount_in if asset_in_address == wbear_address else 0,
             'gasPrice': int(self.w3.eth.gas_price * 1.2), 'nonce': self.get_nonce()})
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
            raise ValueError(
                f'需要授权\nplease run : \nbera.approve_token(bex_approve_liquidity_address, int("0x" + "f" * 64, 16), "{asset_in_address}")')
        txn = self.bex_contract.functions.addLiquidity(pool=pool_address, receiver=self.account.address,
                                                       assetsIn=[asset_in_address],
                                                       amountsIn=[amount_in]).build_transaction(
            {'gas': 500000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def honey_mint(self, amount_usdc_in: int) -> str:
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
            raise ValueError(
                f'需要授权\nplease run : \nbera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), "{usdc_address}")')
        txn = self.honey_swap_contract.functions.mint(to=self.account.address, collateral=usdc_address,
                                                      amount=amount_usdc_in, ).build_transaction(
            {'gas': 500000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def honey_redeem(self, amount_honey_in: int) -> str:
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
            raise ValueError(
                f'需要授权\nplease run : \nbera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), "{honey_address}")')

        txn = self.honey_swap_contract.functions.redeem(to=self.account.address, amount=amount_honey_in,
                                                        collateral=usdc_address).build_transaction(
            {'gas': 500000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def bend_deposit(self, amount_in: int, amount_in_token_address: Union[Address]) -> str:
        """
        bend deposit
        :param amount_in: 数量
        :param amount_in_token_address: 代币地址
        :return:
        """
        amount_in_token_contract = self.w3.eth.contract(address=amount_in_token_address, abi=erc_20_abi)
        token_balance = amount_in_token_contract.functions.balanceOf(self.account.address).call()
        assert token_balance != 0
        assert token_balance >= amount_in
        allowance_balance = amount_in_token_contract.functions.allowance(self.account.address,
                                                                         bend_address).call()
        if allowance_balance < amount_in:
            raise ValueError(
                f'需要授权\nplease run : \nbera.approve_token(bend_address, int("0x" + "f" * 64, 16), "{amount_in_token_address}")')
        txn = self.bend_contract.functions.supply(asset=amount_in_token_address, amount=amount_in,
                                                  onBehalfOf=self.account.address, referralCode=0).build_transaction(
            {'gas': 500000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def bend_borrow(self, amount_out: int, asset_token_address: Union[Address]) -> str:
        """
        bend borrow
        :param amount_out: 数量
        :param asset_token_address: 借款代币地址
        :return:
        """
        txn = self.bend_contract.functions.borrow(asset=asset_token_address, amount=amount_out,
                                                  interestRateMode=2, referralCode=0,
                                                  onBehalfOf=self.account.address).build_transaction(
            {'gas': 500000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def bend_repay(self, repay_amount: int, asset_token_address: Union[Address]) -> str:
        """
        bend 还款
        :param repay_amount:还款数量
        :param asset_token_address: repay 代币地址
        :return:
        """
        allowance_balance = self.honey_contract.functions.allowance(self.account.address, bend_address).call()
        if allowance_balance < repay_amount:
            raise ValueError(
                f'需要授权\nplease run : \nbera.approve_token(bend_address, int("0x" + "f" * 64, 16), "{honey_address}")')

        txn = self.bend_contract.functions.repay(asset=asset_token_address, amount=repay_amount,
                                                 interestRateMode=2, onBehalfOf=self.account.address).build_transaction(
            {'gas': 500000 + random.randint(1, 10000), 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce()})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def honey_jar_mint(self):
        allowance_balance = self.honey_contract.functions.allowance(self.account.address, ooga_booga_address).call()
        if allowance_balance / 1e18 < 4.2:
            raise ValueError(
                f'需要授权\nplease run : \nbera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), "{honey_address}")')
        has_mint = self.ooga_booga_contract.functions.hasMinted(self.account.address).call()
        if has_mint:
            return True
        signed_txn = self.w3.eth.account.sign_transaction(
            dict(
                chainId=80085,
                nonce=self.get_nonce(),
                gasPrice=int(self.w3.eth.gas_price * 1.15),
                gas=134500 + random.randint(1, 10000),
                to=self.w3.to_checksum_address(ooga_booga_address),
                data='0xa6f2ae3a',
            ),
            self.account.key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def deploy_contract(self, contract_source_code, solc_version):
        """
        部署合约
        运行前需要安装你指定的版本
            from solcx import install_solc
            install_solc('0.4.18')
        :param contract_source_code: 合约代码
        :param solc_version: 编译器版本
        :return:
        """
        ""
        set_solc_version(solc_version)
        compiled_sol = compile_source(contract_source_code)
        contract_id, contract_interface = compiled_sol.popitem()
        txn = dict(
            chainId=80085,
            gas=2000000,
            gasPrice=int(self.w3.eth.gas_price * 1.15),
            nonce=self.get_nonce(),
            data=contract_interface['bin'])
        # 签署交易
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

    def create_bera_name(self):
        random_str = ''.join(random.choice(emoji_list) for _ in range(random.randint(5, 20)))
        random_chars = list(random_str)
        random.shuffle(random_chars)
        shuffled_str = ''.join(random_chars)
        txn = self.bera_name_contract.functions.mintNative(chars=list(shuffled_str), duration=1,
                                                           whois=self.account.address,
                                                           metadataURI='https://beranames.com/api/metadata/69',
                                                           to=self.account.address).build_transaction(
            {'gas': 2000000, 'gasPrice': int(self.w3.eth.gas_price * 1.15),
             'nonce': self.get_nonce(), 'value': int(608614232209737)})
        signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=self.private_key)
        order_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return order_hash.hex()

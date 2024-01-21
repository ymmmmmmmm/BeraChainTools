# -*- coding: utf-8 -*-
# Time     :2024/1/21 12:15
# Author   :ym
# File     :contract_config.py
import os

from dotenv import load_dotenv
from web3 import Web3

from config.abi_config import bex_abi, erc_20_abi, honey_abi, bend_abi
from config.address_config import bex_swap_address, honey_swap_address, usdc_address, honey_address, bend_address

load_dotenv()
max_workers = int(os.getenv("MaxWorkers"))
rpc_url = os.getenv("RPC_URL")
w3 = Web3(Web3.HTTPProvider(rpc_url))

bex_contract = w3.eth.contract(address=bex_swap_address, abi=bex_abi)
honey_swap_contract = w3.eth.contract(address=honey_swap_address, abi=honey_abi)
usdc_contract = w3.eth.contract(address=usdc_address, abi=erc_20_abi)
honey_contract = w3.eth.contract(address=honey_address, abi=erc_20_abi)
bend_contract = w3.eth.contract(address=bend_address, abi=bend_abi)

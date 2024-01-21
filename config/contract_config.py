# -*- coding: utf-8 -*-
# Time     :2024/1/21 12:15
# Author   :ym
# File     :contract_config.py
from web3 import Web3

from config.abi_config import bex_abi, erc_20_abi, honey_abi
from config.address_config import bex_swap_address, honey_swap_address, usdc_address, honey_address

w3 = Web3()
bex_contract = w3.eth.contract(address=bex_swap_address, abi=bex_abi)

honey_swap_contract = w3.eth.contract(address=honey_swap_address, abi=honey_abi)
usdc_contract = w3.eth.contract(address=usdc_address, abi=erc_20_abi)
honey_contract = w3.eth.contract(address=honey_address, abi=erc_20_abi)

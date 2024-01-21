# -*- coding: utf-8 -*-
# Time     :2024/1/21 00:19
# Author   :ym
# File     :address_config.py
from web3 import Web3

w3 = Web3()
bex_swap_address = w3.to_checksum_address('0x0d5862FDbdd12490f9b4De54c236cff63B038074')
bend_address = w3.to_checksum_address('0xA691f7CfB3C65A17Dcbf9D6d748Cc677B0640db0')
honey_swap_address = w3.to_checksum_address('0x09ec711b81cD27A6466EC40960F2f8D85BB129D9')
weth_address = w3.to_checksum_address('0x8239FBb3e3D0C2cDFd7888D8aF7701240Ac4DcA4')
honey_address = w3.to_checksum_address('0x7EeCA4205fF31f947EdBd49195a7A88E6A91161B')
usdc_address = w3.to_checksum_address('0x6581e59A1C8dA66eD0D313a0d4029DcE2F746Cc5')
usdc_pool_address = w3.to_checksum_address('0x36Af4FBAb8ebE58b4EfFE0D5d72CeFfc6eFc650A')
usdc_pool_liquidity_address = w3.to_checksum_address('0x5479FbDef04302D2DEEF0Cc78f7D503d81fDFCC9')
weth_pool_liquidity_address = w3.to_checksum_address('0x101f52c804C1C02c0A1D33442ecA30ecb6fB2434')
bex_approve_liquidity_address = w3.to_checksum_address('0x0000000000000000000000000000000000696969')
weth_pool_address = w3.to_checksum_address('0xD3C962F3F36484439A41d0E970cF6581dDf0a9A1')
zero_address = w3.to_checksum_address('0x0000000000000000000000000000000000000000')

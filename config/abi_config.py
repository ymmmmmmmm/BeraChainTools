# -*- coding: utf-8 -*-
# Time     :2024/1/20 23:28
# Author   :ym
# File     :abi_config.py
bex_abi = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "receiver",
                "type": "address"
            },
            {
                "internalType": "address[]",
                "name": "assetsIn",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amountsIn",
                "type": "uint256[]"
            }
        ],
        "name": "addLiquidity",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "shares",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "shareAmounts",
                "type": "uint256[]"
            },
            {
                "internalType": "address[]",
                "name": "liquidity",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "liquidityAmounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IERC20DexModule.SwapKind",
                "name": "kind",
                "type": "uint8"
            },
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "poolId",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "assetIn",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amountIn",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "assetOut",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amountOut",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes",
                        "name": "userData",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct IERC20DexModule.BatchSwapStep[]",
                "name": "swaps",
                "type": "tuple[]"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "batchSwap",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "address[]",
                "name": "assetsIn",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amountsIn",
                "type": "uint256[]"
            },
            {
                "internalType": "string",
                "name": "poolType",
                "type": "string"
            },
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "asset",
                                "type": "address"
                            },
                            {
                                "internalType": "uint256",
                                "name": "weight",
                                "type": "uint256"
                            }
                        ],
                        "internalType": "struct IERC20DexModule.AssetWeight[]",
                        "name": "weights",
                        "type": "tuple[]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "swapFee",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct IERC20DexModule.PoolOptions",
                "name": "options",
                "type": "tuple"
            }
        ],
        "name": "createPool",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "baseAsset",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "quoteAsset",
                "type": "address"
            }
        ],
        "name": "getExchangeRate",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            }
        ],
        "name": "getLiquidity",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "asset",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            }
        ],
        "name": "getPoolName",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            }
        ],
        "name": "getPoolOptions",
        "outputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "address",
                                "name": "asset",
                                "type": "address"
                            },
                            {
                                "internalType": "uint256",
                                "name": "weight",
                                "type": "uint256"
                            }
                        ],
                        "internalType": "struct IERC20DexModule.AssetWeight[]",
                        "name": "weights",
                        "type": "tuple[]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "swapFee",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct IERC20DexModule.PoolOptions",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "name": "getPreviewAddLiquidityNoSwap",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "shares",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "shareAmounts",
                "type": "uint256[]"
            },
            {
                "internalType": "address[]",
                "name": "liqOut",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "liquidityAmounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address[]",
                "name": "liquidity",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "name": "getPreviewAddLiquidityStaticPrice",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "shares",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "shareAmounts",
                "type": "uint256[]"
            },
            {
                "internalType": "address[]",
                "name": "liqOut",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "liquidityAmounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IERC20DexModule.SwapKind",
                "name": "kind",
                "type": "uint8"
            },
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "poolId",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "assetIn",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amountIn",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "assetOut",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amountOut",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes",
                        "name": "userData",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct IERC20DexModule.BatchSwapStep[]",
                "name": "swaps",
                "type": "tuple[]"
            }
        ],
        "name": "getPreviewBatchSwap",
        "outputs": [
            {
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getPreviewBurnShares",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "name": "getPreviewSharesForLiquidity",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "shares",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "shareAmounts",
                "type": "uint256[]"
            },
            {
                "internalType": "address[]",
                "name": "liquidity",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "liquidityAmounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "getPreviewSharesForSingleSidedLiquidityRequest",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IERC20DexModule.SwapKind",
                "name": "kind",
                "type": "uint8"
            },
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "baseAsset",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "baseAssetAmount",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "quoteAsset",
                "type": "address"
            }
        ],
        "name": "getPreviewSwapExact",
        "outputs": [
            {
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "assetIn",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "assetAmount",
                "type": "uint256"
            }
        ],
        "name": "getRemoveLiquidityExactAmountOut",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "assetOut",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "sharesIn",
                "type": "uint256"
            }
        ],
        "name": "getRemoveLiquidityOneSideOut",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            }
        ],
        "name": "getTotalShares",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "withdrawAddress",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "assetIn",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            }
        ],
        "name": "removeLiquidityBurningShares",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "liquidity",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "liquidityAmounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pool",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "withdrawAddress",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "assetOut",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "sharesIn",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "maxSharesIn",
                "type": "uint256"
            }
        ],
        "name": "removeLiquidityExactAmount",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "shares",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "shareAmounts",
                "type": "uint256[]"
            },
            {
                "internalType": "address[]",
                "name": "liquidity",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "liquidityAmounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "enum IERC20DexModule.SwapKind",
                "name": "kind",
                "type": "uint8"
            },
            {
                "internalType": "address",
                "name": "poolId",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "assetIn",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "assetOut",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swap",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "assets",
                "type": "address[]"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]

erc_20_abi = [{"type": "event", "name": "Approval", "inputs": [{"indexed": True, "name": "owner", "type": "address"},
                                                               {"indexed": True, "name": "spender", "type": "address"},
                                                               {"indexed": False, "name": "value", "type": "uint256"}]},
              {"type": "event", "name": "Transfer", "inputs": [{"indexed": True, "name": "from", "type": "address"},
                                                               {"indexed": True, "name": "to", "type": "address"},
                                                               {"indexed": False, "name": "value", "type": "uint256"}]},
              {"type": "function", "name": "allowance", "stateMutability": "view",
               "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}],
               "outputs": [{"name": "", "type": "uint256"}]},
              {"type": "function", "name": "approve", "stateMutability": "nonpayable",
               "inputs": [{"name": "spender", "type": "address"}, {"name": "amount", "type": "uint256"}],
               "outputs": [{"name": "", "type": "bool"}]},
              {"type": "function", "name": "balanceOf", "stateMutability": "view",
               "inputs": [{"name": "account", "type": "address"}], "outputs": [{"name": "", "type": "uint256"}]},
              {"type": "function", "name": "decimals", "stateMutability": "view", "inputs": [],
               "outputs": [{"name": "", "type": "uint8"}]},
              {"type": "function", "name": "name", "stateMutability": "view", "inputs": [],
               "outputs": [{"name": "", "type": "bytes32"}]},
              {"type": "function", "name": "symbol", "stateMutability": "view", "inputs": [],
               "outputs": [{"name": "", "type": "bytes32"}]},
              {"type": "function", "name": "totalSupply", "stateMutability": "view", "inputs": [],
               "outputs": [{"name": "", "type": "uint256"}]},
              {"type": "function", "name": "transfer", "stateMutability": "nonpayable",
               "inputs": [{"name": "recipient", "type": "address"}, {"name": "amount", "type": "uint256"}],
               "outputs": [{"name": "", "type": "bool"}]},
              {"type": "function", "name": "transferFrom", "stateMutability": "nonpayable",
               "inputs": [{"name": "sender", "type": "address"}, {"name": "recipient", "type": "address"},
                          {"name": "amount", "type": "uint256"}], "outputs": [{"name": "", "type": "bool"}]}]

# BeraChainTools

BeraChainTools 一个为 BeraChain 生态系统设计的工具集，旨在帮助用户轻松地进行各种交互和操作。

### 安装依赖

在开始使用 BeraChainTools 之前，请确保安装了所有必要的依赖。

执行以下命令以安装依赖：

```
pip install -r requirements.txt
```

### Examples

- bera目前验证更改为 CloudflareTurnstile，目前支持 yecaptcha 和 2captcha 解码
- 如果你还没有 YesCaptcha 账号，请先在这里注册：[yescaptcha注册链接](https://yescaptcha.com/i/0vVEgw)。
- 如果你还没有 2captcha 账号，请先在这里注册：[2captcha注册链接](https://cn.2captcha.com/?from=9389597)。
- 如果你还没有 ez-captcha
  账号，请先在这里注册：[ez-captcha注册链接](https://dashboard.ez-captcha.com/#/register?inviteCode=djnhuqvHuQJ)。

Example 1 - 领水:

```python
from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools

account = Account.create()
logger.debug(f'address:{account.address}')
logger.debug(f'key:{account.key.hex()}')
# TODO 填写你的 YesCaptcha client key 或者2Captcha API Key 或者 ez-captcha ClientKey
client_key = '00000000000000'
# 使用yescaptcha solver googlev3
bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='yescaptcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
# 使用2captcha solver googlev3
# bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='2captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')
# 使用ez-captcha solver googlev3
# bera = BeraChainTools(private_key=account.key, client_key=client_key,solver_provider='ez-captcha',rpc_url='https://rpc.ankr.com/berachain_testnet')

# 不使用代理
result = bera.claim_bera()
# 使用代理
# result = bera.claim_bera(proxies={'http':"http://127.0.0.1:8888","https":"http://127.0.0.1:8888"})
logger.debug(result.text)
```

Example 2 - Bex 交互:

```python

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import (
    usdc_address, wbear_address, weth_address, bex_approve_liquidity_address,
    usdc_pool_liquidity_address, weth_pool_liquidity_address
)

account = Account.from_key('xxxxxxxxxxxx')
bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

# bex 使用bera交换usdc
bera_balance = bera.w3.eth.get_balance(account.address)
result = bera.bex_swap(int(bera_balance * 0.2), wbear_address, usdc_address)
logger.debug(result)
# bex 使用usdc交换weth
usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
result = bera.bex_swap(int(usdc_balance * 0.2), usdc_address, weth_address)
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

```

Example 3 - Honey 交互:

```python

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import honey_swap_address, usdc_address, honey_address

account = Account.from_key('xxxxxxxxxxxx')
bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

# 授权usdc
approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), usdc_address)
logger.debug(approve_result)
# 使用usdc mint honey
usdc_balance = bera.usdc_contract.functions.balanceOf(account.address).call()
result = bera.honey_mint(int(usdc_balance * 0.5))
logger.debug(result)

# 授权honey
approve_result = bera.approve_token(honey_swap_address, int("0x" + "f" * 64, 16), honey_address)
logger.debug(approve_result)
# 赎回 
honey_balance = bera.honey_contract.functions.balanceOf(account.address).call()
result = bera.honey_redeem(int(honey_balance * 0.5))
logger.debug(result)

```

Example 4 - Bend 交互:

```python

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import bend_address, weth_address, honey_address, bend_pool_address

account = Account.from_key('xxxxxxxxxxxx')
bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

# 授权
approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), weth_address)
logger.debug(approve_result)
# deposit
weth_balance = bera.weth_contract.functions.balanceOf(account.address).call()
result = bera.bend_deposit(int(weth_balance), weth_address)
logger.debug(result)

# borrow
balance = bera.bend_contract.functions.getUserAccountData(account.address).call()[2]
logger.debug(balance)
result = bera.bend_borrow(int(balance * 0.8 * 1e10), honey_address)
logger.debug(result)

# 授权
approve_result = bera.approve_token(bend_address, int("0x" + "f" * 64, 16), honey_address)
logger.debug(approve_result)
# 查询数量 
call_result = bera.bend_borrows_contract.functions.getUserReservesData(bend_pool_address, bera.account.address).call()
repay_amount = call_result[0][0][4]
logger.debug(repay_amount)
# repay
result = bera.bend_repay(int(repay_amount * 0.9), honey_address)
logger.debug(result)

```

Example 5 - 0xhoneyjar 交互:

```python

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address

account = Account.from_key('xxxxxxxxxxxx')
bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')


# https://faucet.0xhoneyjar.xyz/mint
# 授权
approve_result = bera.approve_token(ooga_booga_address, int("0x" + "f" * 64, 16), honey_address)
logger.debug(approve_result)
# 花费4.2 honey mint
result = bera.honey_jar_mint()
logger.debug(result)

```

Example 6 - 部署合约:

```python

from eth_account import Account
from loguru import logger
from solcx import install_solc

from bera_tools import BeraChainTools
from config.address_config import ooga_booga_address, honey_address

account = Account.from_key('xxxxxxxxxxxx')
bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')

# 安装0.4.18 版本编译器
install_solc('0.4.18')
# 读取sol文件
with open('config/WETH.sol', 'r') as f:
  code = f.read()
# 部署合约
result = bera.deploy_contract(code, '0.4.18')
logger.debug(result)

```

Example 7 - 域名注册:

```python

from eth_account import Account
from loguru import logger

from bera_tools import BeraChainTools

account = Account.from_key('xxxxxxxxxxxx')
bera = BeraChainTools(private_key=account.key, rpc_url='https://rpc.ankr.com/berachain_testnet')
result = bera.create_bera_name()
logger.debug(result)

```

### BeraChain 领水

支持创建地址领水或指定地址领水

- **访问链接**：[BeraChain领水](https://artio.faucet.berachain.com/)
- **状态**：已完成

### bex 交互

支持代币交换和增加流动性

- **访问链接**：[bex交互](https://artio.bex.berachain.com/swap)
- **状态**：已完成

### honey 交互

支持mint和redeem

- **访问链接**：[honey交互](https://artio.honey.berachain.com)
- **状态**：已完成

### bend 交互

用于与 BeraChain 的 bend 服务交互。

- **访问链接**：[bend交互](https://artio.bend.berachain.com/)
- **状态**：已完成

### beranames 交互

用于与 BeraChain 的 beranames 服务交互。

- **访问链接**：[beranames交互](https://www.beranames.com)
- **状态**：已完成

### berps 交互

用于与 BeraChain 的 berps 服务交互。

- **访问链接**：[berps交互](https://artio.berps.berachain.com/)
- **状态**：进行中

### station 交互

用于与 BeraChain 的 station 服务交互。

- **访问链接**：[station交互](https://artio.station.berachain.com/)
- **状态**：待完成

---

### galxe 任务

请访问作者
[Fooyao](https://github.com/Fooyao)

- **Github项目地址**：[galxe](https://github.com/Fooyao/galxe_bind_twitter/tree/main)

---


感谢使用
BeraChainTools！如有任何问题或建议，请随时通过 [GitHub Issues](https://github.com/ymmmmmmmm/BeraChainTools/issues) 提交。

如果您认可和喜欢 BeraChainTools 的功能和使用体验，我非常欢迎您给项目点个 star。您的 star 是对我的工作的认可和支持，也是我不断改进和提升
BeraChainTools 的动力！谢谢您的支持！

### 更多疑问请扫码添加好友加入交流群
![微信图片_20240206233445](https://github.com/ymmmmmmmm/BeraChainTools/assets/51306299/52dfc20e-0f11-4fd8-b732-154f38f9b04a)





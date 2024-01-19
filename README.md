
# BeraChainTools

BeraChainTools 一个为 BeraChain 生态系统设计的工具集，旨在帮助用户轻松地进行各种交互和操作。


### 安装依赖

在开始使用 BeraChainTools 之前，请确保安装了所有必要的依赖。

执行以下命令以安装依赖：

```
pip install -r requirements.txt
```

### 配置指南

#### 1. 设置代理

- 打开 `.env` 文件。
- 找到 `PROXY_URL` 并替换成你的代理提取链接。请确保提取格式为文本（text），提取数量设置为1。

  示例：
  ```
  PROXY_URL=http://example.com/get-proxy?nums=1
  ```

#### 2. 设置 YesCaptcha Key

- 如果你还没有 YesCaptcha 账号，请先在这里注册：[yescaptcha注册链接](https://yescaptcha.com/i/0vVEgw)。
- 获取你的 YesCaptcha ClientKey。
- 在 `.env` 文件中找到 `YesCaptchaClientKey` 并填入你的 ClientKey。

  示例：
  ```
  YesCaptchaClientKey=YOUR_CLIENTKEY_HERE
  ```
#### 3. 设置 MaxWorkers(最大工作线程)

- 在 `.env` 文件中找到 `MaxWorkers` 并填入你想要设置的线程数量。

  示例：
  ```
  MaxWorkers=8
  ```
## 功能和使用方法

### BeraChain 领水

drip_tokens.py 
支持创建地址领水或指定地址领水


- **访问链接**：[BeraChain领水](https://artio.faucet.berachain.com/)
- **状态**：已完成

### bex 交互

用于与 BeraChain 的 bex 交互。

- **访问链接**：[bex交互](https://artio.bex.berachain.com/swap)
- **状态**：待完成

### honey 交互

用于与 BeraChain 的 honey 服务交互。

- **访问链接**：[honey交互](https://artio.honey.berachain.com)
- **状态**：待完成

---

感谢使用 BeraChainTools！如有任何问题或建议，请随时通过 [GitHub Issues](https://github.com/ymmmmmmmm/BeraChainTools/issues) 提交。


# 0017. 多联运平台鉴权与动态网关适配器架构

- **状态**: Accepted
- **日期**: 2026-10-16
- **作者**: Ateng

## 背景与问题脉络 (Context)

《神仙道》(SXD) 自心动网络发行以来，采用了经典的联运分销模式 (Syndicated Distribution)：
1. **多平台分销**: 涵盖心动官方 (`xd.com`)、疯玩游戏 (`fengwanyx`)、360、腾讯、百度、4399 等数十家渠道平台；
2. **两层分离架构**:
   - **第一层 (Web 平台鉴权层)**: 各联运平台拥有完全独立的账号数据库、用户鉴权接口、选区页面及单点登录 (SSO) 机制；
   - **第二层 (Socket 协议网关层)**: 无论玩家从哪家联运平台进入，最终大区主站 (`index_wd.php` 或其变体) 返回的底层 TCP 游戏网关服务器 (如 `9x656.sxdweb.xd.com:8381`) 均统一归属于心动官方机房集群，游戏逻辑、Mod/Act 封包结构与业务时序 100% 通用。
3. **架构痛点**:
   - 既有代码中将“疯玩游戏 (`fengwanyx`)”平台的登录接口地址硬编码在 `network/web_auth.py` 中；
   - 当用户游玩其他渠道平台时，因登录地址与鉴权算法不同而无法登录，破坏了架构的通用性与可扩展性。

## 架构决策 (Decision)

我们决定重构网络鉴权模块，采用**策略适配器模式 (Strategy / Adapter Pattern)** 实现多平台解耦：

### 1. 核心抽象与策略注册表
- 定义统一的平台鉴权抽象基类 `BasePlatformAuthProvider`:
  - 核心契约方法：`async auto_login(account: AccountConfig) -> Optional[GatewayCredentials]`
  - 职责：负责平台私有的 Web 凭据校验、选区入场、换取动态 Socket 网关 IP/端口及 Session Token。
- 实现 `PlatformAuthRegistry` 策略注册中心:
  - 依据 `AccountConfig.platform`（平台标识符，如 `fengwanyx`, `xd`, `360`, `static`）动态派发至对应的 Provider 实现；
  - 若配置的平台暂未实现全自动 Web 登录逆向，自动回退至 `StaticAuthProvider`，支持用户通过静态网关直连或 Cookie 模式运行。

### 2. 首批平台 Provider 划分
- **`FengwanAuthProvider` (疯玩游戏 - 默认)**:
  - 维护疯玩平台三步登录流水线：账号凭据鉴权 (`member.fengwanyx.3fangyuan.com`) -> 选区入场 (`play.php`) -> 换取 Socket 网关 (`index_wd.php`)。
- **`StaticAuthProvider` (静态直连 / 通用降级)**:
  - 针对心动官服或其他第三方联运平台用户，只要提供抓包获得的静态网关 (`server_host`, `server_port`) 或会话 Ticket，即刻免逆向直连启动。
- **预留扩展插槽**:
  - `XdOfficialAuthProvider` (心动官服 `xd.com`)，供后续抓包分析或接入时即插即用。

### 3. 动态区服模板与个性化覆盖 (Server URL Templating & Override)
- 各平台 Provider 内部封装该平台的默认区服路由模板（如 `http://{server}.sxd.fengwanyx.com/...`）；
- 允许在 `AccountConfig` 中通过可选参数进行大区入口的静态覆盖，以兼容合服后域名发生迁移的老旧区服。

## 影响评估与向后兼容 (Consequences)

### 正向收益
- **高度解耦与高内聚**: 新增平台只需新增一个独立的 Provider 文件并向注册中心注册，绝不污染存量代码与游戏协议层；
- **故障隔离**: 某一平台的 Web 登录接口变更或失效时，仅影响该平台，其他平台与核心自动化任务丝毫不受影响；
- **全平台兜底保障**: 未逆向全自动登录的平台用户，仍可通过静态网关配置无缝享受 35 大自动化引擎。

### 向后兼容
- 存量配置中缺省 `platform` 或指定 `fengwanyx` 保持 100% 向后兼容；
- 单测与抓包调试使用的 `static_credentials` 模式平滑继承。

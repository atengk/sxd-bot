# 核心基石业务模块精修规范与代码契约 (Player, Town, Item)

> **文档状态**：已冻结 (Frozen)  
> **涵盖模块**：Mod 0 (`Player` 玩家核心), Mod 1 (`Town` 城镇场景), Mod 2 (`Item` 物品背包)  
> **安全防护级别**：包含 `[SAFE_READ]`, `[ROUTINE_FREE]`, `[HAZARDOUS_INGOT]` 三级红线标注  
> **关联工单**：[Ticket 4: 核心基石业务模块精修规范与代码契约](https://github.com/atengk/sxd-bot/issues/5)  
> **上游规约**：[00_binary_framing_and_codecs.md](./00_binary_framing_and_codecs.md) | [01_micro_client_architecture_and_relay.md](./01_micro_client_architecture_and_relay.md) | [02_protocol_index_catalog.md](./02_protocol_index_catalog.md)

---

## 1. 核心基石模块安全红线体系 (Security Invariants)

在对神仙道协议进行无头自动化二次开发时，必须对每个网络动作实施**安全分级管控**，杜绝程序逻辑缺陷导致玩家游戏内珍贵元宝（Ingot）资产被意外扣除：

- `[SAFE_READ]`（只读查询）：纯状态、只读数值拉取，零任何消耗，无副作用，允许高频周期性轮询与重试。
- `[ROUTINE_FREE]`（免费常规）：游戏内的免费例行动作（如角色移动、背包规整、在线礼包免费领取、低级装备变卖换铜钱等），冷却时间满足时可安全执行。
- `[HAZARDOUS_INGOT]`（高危元宝消耗）：涉及真实元宝扣除的操作（如付费购买体力、付费开启背包格位、元宝加速等）。**代码契约层必须内置前置断言保护 (`allow_ingot: bool = False`)**，默认调用时一律抛出安全拦截异常，只有调用方显式传入授权标记且元宝余额充足时方可封包放行。

---

## 2. 模块 0：Mod_Player_Base (玩家角色与登录基石)

`Mod_Player_Base` (Module ID: `0`) 是整套游戏通信的最顶层基石，控制客户端连接握手、防沉迷检测、角色全量属性与数值变更下行广播。

### 2.1 核心动作契约一览

| 动作 ID (`Act`) | 动作名称 | 安全等级 | 核心职责与业务定义 |
| :--- | :--- | :--- | :--- |
| **`0`** | `login` | `[ROUTINE_FREE]` | 客户端 TCP 首帧登录认证，上报微端标识与 Token |
| **`1`** | `player_first_init` | `[ROUTINE_FREE]` | 新角色首次进服初始化 |
| **`2`** | `get_player_info` | `[SAFE_READ]` | 拉取角色基础与高阶 44 维属性全景快照 |
| **`3`** | `update_player_data` | `[SAFE_READ]` | 服务端主动广播的角色数值/资产权威变更通知 |
| **`4`** | `update_player_data_for_town` | `[SAFE_READ]` | 城镇同屏玩家属性与外观变更广播 |
| **`5`** | `buy_power` | `[HAZARDOUS_INGOT]` | **高危**：消耗元宝购买体力（每次 20+ 元宝） |
| **`11`** | `against_wallows_notify` | `[SAFE_READ]` | 防沉迷健康游戏在线时长提醒通知 |
| **`17`** | `player_get_online_gift` | `[ROUTINE_FREE]` | 免费在线时长阶梯礼包领取 |
| **`72`** | `init_client` | `[ROUTINE_FREE]` | 客户端资源预热完成就绪通知（Turn 1 粘包伴随帧） |
| **`99`** | `heartbeat` | `[ROUTINE_FREE]` | 3 秒对齐活跃心跳包 |

---

### 2.2 动作详解与真实十六进制抓包对照

#### Act 0: `login` (登录认证握手)
- **请求字段 (12 项)**：
  - `field_0`: `StringUtil` -> `username` (平台账号名)
  - `field_1`: `StringUtil` -> `hash_code` (32 位 MD5 Token)
  - `field_2`: `StringUtil` -> `time` (时间戳字符串)
  - `field_3`: `StringUtil` -> `platform` (平台代号 `"fengwanyx"`)
  - `field_4`: `IntUtil` -> `0` (保留扩展位)
  - `field_5`: `IntUtil` -> `server_id` (大区数字 ID，如 `25268`)
  - `field_6`: `ByteUtil` -> `is_wd` (是否微端: `1`)
  - `field_7`: `ByteUtil` -> `wd_code` (微端特征标识码: `0x60`)
  - `field_8`: `ByteUtil` -> `sub_code` (`0`)
  - `field_9`: `StringUtil` -> `publish` (平台商标识 `"疯玩"`)
  - `field_10`: `StringUtil` -> `client_type` (`"pc_wd"`)
  - `field_11`: `ByteUtil` -> `flag` (`1`)
- **真实抓包切片 (Stream 18 Turn 1 复合前帧, 108 字节)**：
  ```text
  000000680000000000066b6f6e6779750020623437373635393362623834386537623634
  6638386139386465623431613863000a31373932303635333835000966656e6777616e79
  7800000000000062b40160000006e796afe78ea9000570635f77640100066b6f6e677975
  ```
- **应答字段 (官方 10 字段标准契约)**：
  `[UByteUtil, IntUtil, UByteUtil, IntUtil, ByteUtil, IntUtil, ByteUtil, UByteUtil, IntUtil, ByteUtil]`
  - `status`: 0=成功，1=失败，2=首次登录，3=防沉迷限制
  - `player_id`: 角色唯一数值 ID (抓包中为 `4`)
- **真实抓包切片 (Stream 18 Turn 2, 30 字节)**：
  ```text
  0000001a0000000000000000040a000000000000000001000b0000108501
  ```

#### Act 2: `get_player_info` (角色基础属性 44 维全景契约)
- **请求字段**：无 (`req=[]`)
- **应答字段 (精选核心字段映射)**：
  - `[0] StringUtil`: 角色昵称 (如 `"梦一场"`)
  - `[1] IntUtil`: 当前真实等级 (如 `300`)
  - `[2] IntUtil`: 当前持有元宝 (Ingot)
  - `[3] LongUtil`: 当前持有铜钱 (8 字节 64 位整型)
  - `[4] LongUtil`: 当前生命值 (Health)
  - `[5] LongUtil`: 生命值上限 (Max Health)
  - `[6] IntUtil`: 当前体力点数 (Power)
  - `[7] LongUtil`: 当前角色经验值
  - `[8] LongUtil`: 升级所需经验上限
  - `[9] IntUtil`: 当前所在城镇地图编号 (Town ID，如 `29` 大理城)
  - `[14] IntUtil`: VIP 等级
  - `[21] IntUtil`: 角色声望 (Fame)
  - `[29] IntUtil`: 当前已解锁最高精英/普通副本关卡 ID

#### Act 3: `update_player_data` (资产与数值权威动态下行更新)
- **请求格式**：`[UByteUtil]` (主动查询指定属性) 或由服务端事件主动推送
- **应答载荷结构**：`[2B 计数 N]` + N × `[1B 属性 ID (PropID) + 8B 属性值 (64位大端整型)]`
- **高频权威属性 ID 对照字典**：
  - `18`: 角色等级 (Level)
  - `19`: 角色元宝余额 (Ingots)
  - `20`: 角色铜钱余额 (Coins)
  - `23` / `77`: 角色当前体力 (Power)
  - `37`: 角色当前声望 (Fame)
  - `39`: VIP 等级

---

## 3. 模块 1：Mod_Town_Base (城镇场景与寻路移动基石)

`Mod_Town_Base` (Module ID: `1`) 负责玩家在世界地图与各城镇主城场景内的进入、离线、同屏玩家拉取与坐标同步。

### 3.1 核心动作契约一览

| 动作 ID (`Act`) | 动作名称 | 安全等级 | 核心职责与业务定义 |
| :--- | :--- | :--- | :--- |
| **`0`** | `enter_town` | `[ROUTINE_FREE]` | 进入指定城镇场景，获取城镇 NPC、传送门与同屏玩家快照 |
| **`1`** | `leave_town` | `[ROUTINE_FREE]` | 离开当前城镇场景 |
| **`2`** | `move_to` | `[ROUTINE_FREE]` | 在城镇场景内沿网格坐标移动寻路 |
| **`3`** | `get_players` | `[SAFE_READ]` | 主动拉取当前城镇同屏在线玩家列表 |
| **`4`** | `player_follow_role_change`| `[ROUTINE_FREE]` | 切换城镇展示的跟随角色/坐骑外观 |

---

### 3.2 动作详解与结构定义

#### Act 0: `enter_town` (进入城镇)
- **请求字段**：`[IntUtil: town_id]`（目标城镇编号，如 1=小渔村, 2=苏州城, 29=大理城）
- **应答格式**：包含同屏角色列表与地图属性的大型复合报文。首字节为状态码：
  - `0`: `SUCCESS` (进入成功)
  - `1`: `FAILED` (进入失败)
  - `2`: `FULL` (城镇场景人数已满)
  - `7`: `TOWN_HIDDEN` (隐藏场景)

#### Act 2: `move_to` (场景移动寻路)
- **请求字段 (4 项 16 位整型坐标)**：
  - `src_x`: `ShortUtil` (起点 X 网格坐标)
  - `src_y`: `ShortUtil` (起点 Y 网格坐标)
  - `dst_x`: `ShortUtil` (目标 X 网格坐标)
  - `dst_y`: `ShortUtil` (目标 Y 网格坐标)
- **应答回执**：`[IntUtil: player_id, ShortUtil: src_x, ShortUtil: src_y, ShortUtil: dst_x, ShortUtil: dst_y]`

---

## 4. 模块 2：Mod_Item_Base (背包、装备与物品资产基石)

`Mod_Item_Base` (Module ID: `2`) 控制角色主背包（Pack）、随身仓库（Warehouse）、穿戴装备栏、道具变卖与格位扩容。包含全游戏最关键的物品资产操作。

### 4.1 核心动作契约一览

| 动作 ID (`Act`) | 动作名称 | 安全等级 | 核心职责与业务定义 |
| :--- | :--- | :--- | :--- |
| **`1`** | `get_item_basical_infos` | `[SAFE_READ]` | 获取全物品基础模板元数据 (名称、分类、买卖价格) |
| **`2`** | `get_empty_grid_number` | `[SAFE_READ]` | 查询主背包当前剩余可用空格数量 |
| **`3`** | `get_all_player_item_infos`| `[SAFE_READ]` | 获取玩家当前背包与已装备物品完整快照 |
| **`41`** | `get_player_pack_item_list`| `[SAFE_READ]` | 获取主背包当前物品列表及格位堆叠详情 |
| **`44`** | `change_pack_item_grid` | `[ROUTINE_FREE]` | 在背包内部拖拽置换物品格位 |
| **`46`** | `drop_pack_grid_item` | `[ROUTINE_FREE]` | 丢弃背包指定格位物品（销毁） |
| **`48`** | `move_warehouse_grid_item_to_pack` | `[ROUTINE_FREE]` | 从仓库将物品取出至主背包 |
| **`49`** | `move_pack_grid_item_to_warehouse` | `[ROUTINE_FREE]` | 将主背包物品存入仓库 |
| **`50`** | `equip_player_role_item` | `[ROUTINE_FREE]` | 为指定伙伴角色穿戴武器或防具装备 |
| **`51`** | `remove_player_role_equipment` | `[ROUTINE_FREE]` | 卸下指定伙伴角色身上的穿戴装备 |
| **`52`** | `classify_pack` | `[ROUTINE_FREE]` | **一键背包智能自动归纳排序** |
| **`53`** | `classify_warehouse` | `[ROUTINE_FREE]` | 一键仓库智能自动归纳排序 |
| **`54`** | `add_pack_grid` | `[HAZARDOUS_INGOT]` | **高危**：消耗元宝解锁新的背包格子 |
| **`55`** | `add_warehouse_grid` | `[HAZARDOUS_INGOT]` | **高危**：消耗元宝解锁新的仓库格子 |
| **`58`** | `player_sell_item` | `[ROUTINE_FREE]` | **杂物变卖**：批量出售低级无用物品回收铜钱 |

---

### 4.2 动作详解与安全防御规则

#### Act 52: `classify_pack` (一键背包智能整理)
- **请求字段**：无 (`req=[]`)
- **应答字段**：`[UByteUtil: status_code]`
  - `20`: `ACTION_SUCCESS` (整理成功)
  - `143`: `ACTION_FAILED` (整理失败)
- **安全性**：`[ROUTINE_FREE]`，零元宝开销，日常例程可无条件安全执行。

#### Act 58: `player_sell_item` (物品变卖换取铜钱)
- **请求字段**：`[IntUtil: player_item_id]` (玩家背包格子物品唯一实例 ID)
- **应答字段**：`[UByteUtil: result_code, IntUtil: return_coins]`
  - `20`: `ACTION_SUCCESS` (出售成功，返回回收铜钱金额)
- **安全防范策略**：调用前必须前置校验目标物品品质，严禁变卖紫色或橙色品质以上装备，仅允许变卖白色、灰色装备与低级通关材料。

#### Act 54: `add_pack_grid` (元宝解锁背包格子) - `[HAZARDOUS_INGOT]`
- **请求字段**：`[IntUtil: grid_count]` (需要扩容解锁的格子数)
- **应答字段**：`[UByteUtil: result_code]`
- **强制安全守卫契约**：
  ```python
  # 契约代码前置防御逻辑
  if not allow_ingot:
      raise PermissionError("[HAZARDOUS_INGOT] add_pack_grid 涉及元宝扣除，已触发安全熔断保护！若确认执行请显式设置 allow_ingot=True")
  ```

---

## 5. 二次开发落地指导与代码使用

在自动化开发中，所有三大基石模块均可通过 `protocol.messages.*` 导入手撕精修强类型模型进行交互：

```python
from protocol.messages.player import PlayerLoginReq, PlayerInfoResp
from protocol.messages.town import TownEnterTownReq, TownMoveToReq
from protocol.messages.item import ItemClassifyPackReq, ItemSellItemReq, ItemAddPackGridReq

# 1. 场景移动 (零风险例行)
move_packet = TownMoveToReq(src_x=120, src_y=80, dst_x=150, dst_y=90)
client.send_packet(move_packet)

# 2. 一键整理背包 (零风险例行)
classify_packet = ItemClassifyPackReq()
client.send_packet(classify_packet)

# 3. 扩充背包 (元宝高危 - 前置拦截测试)
try:
    danger_packet = ItemAddPackGridReq(grid_count=5) # 默认 allow_ingot=False
except PermissionError as exc:
    logger.info("成功拦截未授权的元宝扣除操作: %s", exc)
```

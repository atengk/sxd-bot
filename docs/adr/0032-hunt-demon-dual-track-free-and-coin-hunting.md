# 32. 每日猎妖双轨全额猎捕 (免费 5 次 + 铜钱 15 次)、防破产底线与零元宝死锁决策

## 状态
已接受 (Accepted) - 2026-10-17

## 背景与问题陈述
猎妖系统 (Mod 105: `Mod_HuntDemon_Base`) 是神仙道产出关键器灵材料、命格经验以及大量历练的核心日常活动。
经官方协议逆向、协议数据库 (`data/protocol_manifest.db`) 检索与真机回包探测，此前猎妖日常实现存在以下核心缺陷：
1. **铜钱猎妖完全缺失**：
   - 官方协议 `open_hunt_demon` 回包格式为 `[Byte, Byte, Byte, Short, ...]`:
     - Byte 1: 剩余免费猎妖次数 `free_times` (每日上限 5 次)；
     - Short 3-4: 剩余可用铜钱猎妖次数 `coin_times` (每日上限 15 次)；
   - 原代码仅读取了前 3 个单字节，并在 `free_times <= 0` 时直接提前退出，导致每日 15 次高价值铜钱猎妖从未触发；
2. **缺乏铜钱防破产安全底线**：
   - 铜钱猎妖每轮需要消耗铜钱。若针对铜钱存量极低的新号或耗尽铜钱的账号盲目执行，可能导致角色铜钱被彻底清空；
3. **缺乏背包满状态主动熔断**：
   - 猎妖会产出各类妖兽材料与掉落物。当背包满 (`PACK_FULL = 6`) 时若不主动熔断，将导致后续循环全部返回异常。

## 决策内容

### 1. 协议模型与入参规范 (Mod 105)
经直接反编译官方微端 ActionScript (`HuntDemonView` 与 `HuntDemonData`) 完整还原真实二进制契约：
- **面板同步 (`open_hunt_demon`, Act 1)**：
  - 发送 `PacketBuilder(mod=105, act=1).write_int8(0).build()`；
  - 响应提取（严格对齐 `HuntDemonData.open_hunt_demon` 字段映射）：
    - Byte 0: 剩余免费猎妖次数 `free_times`；
    - Byte 1: 剩余可用铜钱猎妖次数 `coin_times`；
    - Byte 2: 剩余元宝猎妖次数 `ingot_times`；
    - Short 3-4: 每次元宝猎妖所需元宝数 `need_ingot`；
- **挑战动作 (`hunt_demon`, Act 2)**：
  - 免费猎妖：`type = 0` (`HUNT_MODE_FREE`，对应客户端 `sendFreeFun`)，`auto_buy = 0`；
  - 铜钱猎妖：`type = 1` (`HUNT_MODE_COIN`，对应客户端 `sendCommonFun`)，`auto_buy = 0`；
  - 元宝猎妖：`type = 2` (`HUNT_MODE_INGOT`，对应客户端 `sendIngotFun`，**严守红线，坚决不调用**)；
  - **零元宝死锁红线**：`auto_buy` 参数 100% 硬编码为 `0`，坚决不消耗任何元宝购买挑战次数。

### 2. 双轨递进式执行流水线 (Two-Phase Execution Pipeline)
1. **第一阶段：免费猎妖 (Free Hunt)**：
   - 当 `free_times > 0` 时，循环下发 `hunt_demon(type=0, auto_buy=0)`；
   - 捕获 `SUCCESS (5)` 计入成功；捕获 `PACK_FULL (6)` 记录告警并立即全流程熔断；捕获 `NO_ENOUGH_TIMES (9)` / `NO_ENOUGH_INGOT (7)` 优雅结束免费阶段；
2. **第二阶段：铜钱猎妖 (Coin Hunt)**：
   - 当 `coin_times > 0` 且未触发背包满时执行；
   - **防破产卫语句**：每次下发前检查 `ctx.player.coins >= MIN_COIN_THRESHOLD (500,000)`，低于底线立即退出保护资产；
   - 循环下发 `hunt_demon(type=1, auto_buy=0)`；
   - 捕获 `SUCCESS (5)` 计入成功；捕获 `NO_ENOUGH_COIN (8)` 或 `NO_ENOUGH_TIMES (9)` 优雅退出；捕获 `PACK_FULL (6)` 立即中止。

### 3. 向后兼容与遥测规范
- 任务执行结果 `TaskResult.data` 同时保留存量字段 `hunts_done` 与精细化字段 `total_hunts`、`free_hunts_done`、`coin_hunts_done`、`free_times_left`、`coin_times_left`、`pack_full`，完全杜绝破坏性变更。

## 影响评估
- **收益**：每日全额吃透全部免费猎妖 + 铜钱猎妖，妖兽材料与历练收益最大化。
- **安全**：零元宝硬编码死锁、50万铜钱防破产底线与背包满熔断三合一护航。

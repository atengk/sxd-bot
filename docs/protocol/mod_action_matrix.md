# 神仙道无头协议二进制封包规约速查矩阵 (Protocol & Action Matrix)

本文档系统汇总了神仙道微端 Flash 客户端逆向还原的核心二进制业务协议，包含各功能模块号 (Mod)、动作号 (Act)、大端序封包结构契约与安全防御准则。

---

## 1. 传输层封包物理结构规范

所有发往服务端的请求帧以及服务端推送回包均遵循统一的物理帧格式：

```text
+-------------------+------------------+------------------+-----------------------+
| 4 Bytes Length    | 2 Bytes Mod      | 2 Bytes Act      | N Bytes Payload       |
| (Big-Endian UInt) | (Big-Endian U16) | (Big-Endian U16) | (Flash ByteArray)     |
+-------------------+------------------+------------------+-----------------------+
```

- **Length (4 字节大端整数)**：`len(Mod + Act + Payload)`，即 4 + 业务载荷字节数。
- **Mod (2 字节大端短整数)**：业务模块编号。
- **Act (2 字节大端短整数)**：模块内部细分动作指令。
- **Payload**：业务有效载荷。若包体前两字节命中 RFC 1950 zlib 签名（`0x78` 配合 `0x01`/`0x5E`/`0x9C`/`0xDA`），则上层解析前必须由 `FrameFSM` 状态机执行流式解压。

---

## 2. 核心基础设施协议

### 2.1 登录握手与凭据校验 (Mod 0: `Mod_Player_Base`)

| 动作指令 (Act) | 十进制 / 十六进制 | 对应方法名 | 请求体字段结构 (Request Payload) | 回包字段结构 (Response Payload) |
| :--- | :--- | :--- | :--- | :--- |
| **Act 0** | `0 / 0x0000` | `login_req` | `write_utf(username)`<br>`write_utf(hash_token)`<br>`write_int32(server_id)`<br>`write_utf(client_version)` | `read_uint8(status)` (0:成功, 1:密码错, 2:封号)<br>`read_int32(player_id)`<br>`read_utf(nickname)` |
| **Act 72** | `72 / 0x0048` | `init_client` | `write_int32(0)` | 服务端确认包 (状态同步) |
| **Act 99** | `99 / 0x0063` | `verify_ver` | `write_int32(72)` | 版本匹配回执 |
| **Act 2** | `2 / 0x0002` | `get_player_info` | `write_int32(99)` | `read_int32(player_id)`<br>`read_utf(name)`<br>`read_int32(level)`<br>`read_int64(coins)`<br>`read_int32(ingots)`<br>`read_int32(town_id)` |

### 2.2 传输层高频活性心跳保活 (Mod 184)

| 动作指令 (Act) | 十进制 / 十六进制 | 对应方法名 | 请求体字段结构 | 周期与超时规则 |
| :--- | :--- | :--- | :--- | :--- |
| **Act 4** | `4 / 0x0004` | `heartbeat_tick` | 空载荷 (仅 4 字节长度头 + Mod 184 + Act 4) | 推荐间隔 **3.0 秒**。若超过 15 秒无任何发包，服务端网关将主动 RST/EOF 切断连接。 |

---

## 3. 日常福利与挂机玩法协议矩阵

### 3.1 招财神符 (Mod 76: `Mod_MoneyTree_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询招财神符状态 | 空 | 返回包含 `free_count` (剩余免费次数) 与 `cost_ingots`。 |
| **Act 1** | 领取/抽取神符 | 空 | **安全红线**：仅当 `free_count > 0` 时方可发送；若免费次数耗尽，服务端将扣除元宝，框架必须前置拦截。 |

### 3.2 帮派祭神 (Mod 21: `Mod_WorshipMars_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询神像状态 (`mars_info`) | 空 (0 字节) | 返回 24 字节大端整数数组：`[reserve0, god_level, reserve1, reserve2, free_times, max_times]`。其中 `free_times` 为今日剩余免费祭神次数。 |
| **Act 1** | 祭神上香 (`incense`) | `write_uint8(incense_type)`<br>`1: 白檀香 (消耗微量铜钱, 零元宝)`<br>`2: 苏合香 (消耗元宝, 坚决禁止)`<br>`3: 天木香 (消耗大额元宝, 坚决禁止)` | **安全红线**：仅当 `free_times > 0` 且上香参数必须严格硬编码为 `1` (白檀香)；若免费次数归零立即触发零元宝熔断并跳过。获得声望 +100，帮派贡献 +10 与攻击祝福。 |

### 3.3 吉星高照 (Mod 38: `Mod_RollCake_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 2** | 查询吉星高照状态 | `00e40000` (状态标记) | 返回剩余免费掷骰次数、当前骰子锁定状态与当前境界点收益。 |
| **Act 0** | 投掷吉星骰子 | 动态骰子索引数组 | 同步最新境界点数值至 `GameContext`。 |

### 3.4 仙府药园 (Mod 13: `Mod_Farm_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 刷新土地与仙草状态 | `01b10002` (药园协议指纹) | 返回各土地编号、种植仙草类型、剩余成熟秒数及除草/浇水状态。 |
| **Act 1** | 收获成熟仙草 | `write_int32(land_id)` | 成功结算大量经验或铜钱，土地状态置空。 |

### 3.5 摘仙桃与神龙拜祭 (Mod 100 / Mod 40)

| 模块与动作 | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Mod 100, Act 45** | 查询仙桃果实状态 | 空 | 返回今日可摘仙桃树等级与剩余摘取机会。 |
| **Mod 100, Act 34** | 一键摘取仙桃 | 空 | 结算巨额角色升级经验。末字节为状态位（`1` 表示成功）。 |
| **Mod 100, Act 29** | 神龙抚养与拜祭 | 空 | 免费提升神龙祝福与帮派活跃度，零元宝消耗。 |

### 3.6 猎命系统 (Mod 41: `Mod_Fate_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询猎命师与猎命背包状态 | `02700001` (猎命指纹) | 返回 5 位猎命师点亮状态及命盘空位。 |
| **Act 4** | 一键变卖厄运灰命 | `0088000a` | 自动将命格临时包中的所有灰色厄运命格转化为铜钱，释放格子。 |
| **Act 2** | 一键拾取命格入包 | `00290004` | 自动将绿色、蓝色、紫色、金色命格拾取进角色命格背包。 |

### 3.7 七日登录与常规签到 (Mod 127 / Mod 42)

| 模块与动作 | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Mod 42, Act 0** | 查询常规每日签到 (`get_sign_in_info`) | 空 (0 字节) | 返回 11 字节：`signed_days(U16)` + `is_today_signed(U8: 0=未签, 1=已签)` + `timestamp(8B)`。 |
| **Mod 42, Act 2** | 执行常规签到 (`player_sign_in`) | 空 (0 字节) | 仅当 `is_today_signed == 0` 时调用，领取铜钱、声望与灵石。 |
| **Mod 127, Act 0** | 查询七日礼包列表 (`get_player_sign_in_info_two`) | 空 (0 字节) | 返回 `total_items(U16)` + 循环 `[award_id(U16), status(U8: 0=可领, 1=已领)]`。 |
| **Mod 127, Act 2** | 领取指定项七日礼包 | `write_uint16(item_idx)` | 针对 `status == 0` 的项发送即时入包指令。 |

### 3.8 在线时长礼包、微端专享礼包与阵营俸禄 (Mod 0: `Mod_Player_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Mod 0, Act 39** | 领取微端专享礼包 (`receive_client_gift`) | `write_int32(0)` | 每日一次，微端登录专属福利，获得铜钱、体力与阅历。 |
| **Mod 0, Act 46** | 领取在线时长礼包 (`player_get_online_gift`) | `write_int32(0)` | 累积在线达到档位时领取免费材料礼包。 |
| **Mod 0, Act 22** | 领取阵营/帮派每日俸禄 (`get_player_camp_salary`) | `write_bytes(00010000)` | 每日一次，按角色等级与官职结算海量铜钱俸禄。 |

### 3.9 仙履奇缘 (Mod 100: `Mod_TravelEvent_Base`)

| 模块与动作 | 说明 | 决策策略 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Mod 100, Act 0** | 奇遇问答交互 | 选项索引 `1` 或 `2` | 依据内置策略字典答题（收益优先级：**体力 > 声望 > 经验 > 铜钱**）。禁止消耗元宝清除答题冷却。 |

---

## 4. 战斗与副本挑战协议矩阵

### 4.1 竞技场冲榜 (Mod 28: `Mod_SuperSport_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与战报格式 |
| :--- | :--- | :--- | :--- |
| **Act 3** | 打开竞技场面板 | 空 | 初始化天梯排名与剩余挑战次数。 |
| **Act 4** | 获取可挑战对手列表 | 空 | 返回对手排名、昵称、等级与战斗力列表。 |
| **Act 9** | 发起竞技场挑战 | `write_int32(target_player_id)` | **软柿子选择策略**：选取排名靠前但战斗力低于我方的目标；服务端秒回战报（实测 176 字节二进制），胜者获得 10 声望。 |

### 4.2 每日精英副本扫荡 (Mod 7: `Mod_HeroMission_Base`)

| 动作指令 (Act) | 说明 | 前置安全门槛 | 业务逻辑 |
| :--- | :--- | :--- | :--- |
| **Act 0 / Act 2** | 精英副本查询与扫荡 | 角色等级 ≥ 15 级 | 自动巡检剩余次数并扫荡，若已达今日上限或处在非副本城镇则友好跳过 (`SKIPPED`)，避免触发网关非法地图断连。 |

### 4.3 多人副本限时挑战 (Mod 14: `Mod_MultipleMission_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 时段门槛与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 打开多人副本面板 | 空 | **活动时段感知**：仅在每日 **12:30-13:30** 与 **18:30-19:30** 开启。非活动时段前置跳过。 |
| **Act 5** | 加入现有队伍 | `write_int32(team_id)` | 优先加入已有队伍直接混队通关。 |
| **Act 3** | 自动创建队伍 | `write_int32(mission_id)` | 若无现成队伍，自动创建并等待路人加入。 |

### 4.4 世界 Boss 巨兽挑战 (Mod 24: `Mod_WorldBoss_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 时段门槛与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 15** | 战力鼓舞 | `write_uint8(type=1)` (阅历鼓舞) | **活动时段**：每日 **10:00** (刀疤兔) 与 **15:30** (赤炎兽)。**严禁元宝鼓舞**，仅使用阅历提升伤害。 |
| **Act 14** | 发起 Boss 战斗 | 空 | 挑战 Boss 并同步伤害累积。 |
| **Act 13** | 阵亡复活 | `write_uint8(free=1)` | 仅使用免费复活或等待冷却计时，坚决不扣元宝秒复活。 |

### 4.5 普通副本体力极速扫荡 (Mod 25: `Mod_MissionPractice_Base`)

> [!IMPORTANT]
> **官方 ActionScript 契约确认（绝不带多余伪指令与冗余 Hex）**：
> 极速秒完成（`quickly`）结算后，服务端已自动下发战报并关闭倒计时，**严禁再次调用 `cancel_practice`**，否则服务端判定当前未处于扫荡状态而主动下发 EOF 切断长连接。

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与状态定义 (Response Payload) |
| :--- | :--- | :--- | :--- |
| **Mod 25, Act 0** | 查询关卡扫荡信息 (`get_practice_info`) | `write_int32(mission_id)` | `[2B Short] + [[4B Int, 2B Short, 1B Byte]] + [1B Byte] + [8B Long]` 关卡历史状态与挂机产出。 |
| **Mod 25, Act 1** | 启动全额扫荡 (`start_practice`) | `write_int32(mission_id)`<br>`write_uint16(times=0)` (0 表示消耗全部剩余体力)<br>`write_uint8(auto_sale=1)` (1 开启杂物变卖) | `[1B result] + [4B remain_time] + [4B finish_time]`<br>状态码：`0`=成功 (`SUCCESS`), `1`=体力不足 (`NOT_ENOUGH_POWER`), `2`=背包已满 (`BAG_FULL`)。 |
| **Mod 25, Act 3** | 免费极速秒完成 (`quickly`) | `write_uint16(times=0)` (0 极速完成全部轮次) | `[1B result] + [2B remain_time]`<br>跳过倒计时排队，服务端即刻计算全部场次并连续推送战报与掉落。 |
| **Mod 25, Act 4** | 扫荡掉落与经验广播 (`notify`) | 被动下发广播 | 逐场推送战斗经验、铜钱收益与低阶杂物自动变卖明细。 |
| **Mod 0, Act 3** | 角色体力与属性变更广播 (`update_player_data`) | 被动下发 (大端键值流) | 权威下发：`PropID=23/77` (体力), `18` (等级), `19` (元宝), `20` (铜钱), `37` (声望), `39` (VIP)。 |

### 4.6 竞技场冲榜与零元宝安全熔断 (Mod 28: `Mod_SuperSport_Base`)

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 28, Act 13** | 查询剩余免费挑战次数 (`get_challenge_times`) | 空载荷 (`PacketBuilder(mod=28, act=13).build()`) | `[2B Short free_times]`：剩余免费挑战次数。**强安全卫语句**：若 `free_times <= 0` 立即安全跳过，坚决不付费购买额外次数。 |
| **Mod 28, Act 12** | 查询挑战冷却时间 (`get_cd_time`) | 空载荷 | `[4B Int cd_time]`：冷却剩余秒数。若 `cd_time > 0` 安全跳过，坚决不花元宝秒 CD。 |
| **Mod 28, Act 1** | 拉取候选对手列表 (`get_challenge_list`) | 空载荷 | `[[4B TargetPlayerId, ...]]`：候选挑战玩家列表。 |
| **Mod 28, Act 2** | 发起挑战 (`start_challenge`) | `write_int32(target_player_id)` | 即时战斗结算并下发声望奖励。 |

### 4.7 仙府药园最新官方协议契约 (Mod 13: `Mod_Farm_Base`)

> **官方反编译与实机抓包确认**：
> 服务端已全量演进为新版仙府药园体系（`Act 21-26`），老旧 `Act 0/6` 接口仅保留兼容视图。

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 13, Act 21** | 获取已开垦土地列表 (`get_new_farmlandinfo_list`) | 空载荷 (`PacketBuilder(mod=13, act=21).build()`) | `[2B count]` + 数组元素（每块土地固定 19 字节）：<br>- `4B Int farmland_id` (土地物理编号，如 10, 11, 12, 8)<br>- `4B Int herbs_id` (作物种子 ID，0 为未种植)<br>- `4B Int farmland_time` (成熟倒计时秒数，0 为成熟可收)<br>- `1B UByte farmland_level` (土地品阶)<br>- `1B UByte is_plant` (种植就绪标识)<br>- `5B Extra` 扩展属性。 |
| **Mod 13, Act 22** | 获取可用仙草种子列表 (`new_farmland_herbs_list`) | 空载荷 | `[2B count]` + 数组（每种 20 字节）：`4B seed_id, 4B name_id, 4B lvl, 4B reward, 4B extra`（默认优先播种 169 经验草或 175 铜钱草）。 |
| **Mod 13, Act 24** | 土地播种仙草 (`plant_new_herbs`) | `write_int32(farmland_id)`<br>`write_int32(seed_id)` | 回包 27 字节：`1B result (8=SUCCESS) + 4B farmland_id + 4B herbs_id + 4B level ...`。 |
| **Mod 13, Act 25** | 成熟仙草单倍收获 (`harvest_new`) | `write_int32(farmland_id)` | 回包 `1B result (8=SUCCESS) + 4B remain_exp + ...`。**强安全红线**：严禁调用双倍或元宝催熟，杜绝元宝消耗。 |
| **Mod 13, Act 19** | 探查每日仙令礼包 (`is_player_get_xian_ling_gift`) | 空载荷 | `1B Byte`：非 0 表示有未领取的仙令福利。 |
| **Mod 13, Act 20** | 领取每日仙令礼包 (`player_get_xian_ling_gift`) | 空载荷 | `2B` 礼包领奖状态标识。 |

### 4.8 吉星高照最新官方协议契约 (Mod 38: `Mod_RollCake_Base`)

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 38, Act 2** | 查询剩余免费次数与境界点 (`get_count`) | 空载荷 (`PacketBuilder(mod=38, act=2).build()`) | `[2B Short free_times] + [2B Short points] + [4B Int extra_points]`（剩余免费投掷次数、当前积分与累计境界点收益）。<br>**强前置卫语句**：若 `free_times <= 0` 立即安全熔断，**绝对严禁调用 `Act 3 (reroll)` 消耗元宝改命或花元宝购买挑战次数**。 |
| **Mod 38, Act 4** | 结算并领取吉星奖励 (`get_award`) | 空载荷 | `1B Byte result`：`0`=成功 (`SUCCESS`), `4`=暂无记录 (`NO_RECORD`)。 |
| **Mod 38, Act 5** | 激活并获取吉星状态 (`get_state`) | 空载荷 | `12B` 状态向量：`1B status + 11B params`。 |
| **Mod 38, Act 0** | 免费投掷吉星 (`roll`) | 空载荷 | `10 项结构流`（含骰子点数与即时产出）。投掷后即刻调用 `Act 4` 领奖入库。 |
| **Mod 38, Act 6/7** | 自动吉星状态与配置 (`is_auto` / `set_auto`) | `write_uint8(1)` 开启自动 | 查询与设置自动吉星流。 |

### 4.9 齐天大圣摘仙桃最新官方协议契约 (Mod 40: `Mod_GetPeach_Base`)

> **官方反编译与实机抓包确认**：
> 官方微端核心偷桃模块位于 `Mod 40` (`Mod_GetPeach_Base`)。

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 40, Act 3** | 查询仙桃基础信息 (`peach_info`) | 空载荷 (`PacketBuilder(mod=40, act=3).build()`) | `[4B status]` 仙桃成熟度与轮次标识。 |
| **Mod 40, Act 4** | 查询角色偷桃进度 (`player_info`) | 空载荷 | `[13B payload]` 角色当前桃树层级与待摘仙桃总数。 |
| **Mod 40, Act 5** | 一键批量摘仙桃 (`batch_get_peach`) | 空载荷 | `[1B result (0=SUCCESS)] + [4B extra] + [4B exp]`<br>秒级结算所有待摘仙桃，单次实测获取海量升级经验 (高达数千万至数十亿经验)，严格零元宝。 |
| **Mod 40, Act 6** | 召唤/结算白猿仙桃 (`call_peach`) | 空载荷 | `[1B result (0=SUCCESS)]`。 |
| **Mod 40, Act 2** | 元宝购买猴子 (`buy_monkeys`) | **绝对禁止调用** | **强安全红线**：单次消耗 50 元宝，必须在任何代码中前置阻断！ |

### 4.10 喜从天降与通商最新官方协议契约 (Mod 41: `Mod_Traders_Base`)

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 41, Act 0** | 查询通商主面板 (`get_panel_info`) | 空载荷 (`PacketBuilder(mod=41, act=0).build()`) | `239 字节` 主面板结构：包含 5 大港口货物价格、汇率、当前代币与资产仓位上限。 |
| **Mod 41, Act 2** | 查询通商日常状态 (`daily_info`) | 空载荷 | `[4B daily_val] + [4B daily_cnt]` 通商积分与可用次数。 |
| **Mod 41, Act 4** | 最新行情趋势指数 (`latest_trend`) | 空载荷 | `[4B trend_index]` 市场物价涨跌指数与风向标。 |
| **Mod 41, Act 5** | 赛季窗口与排行榜 (`term_rank`) | 空载荷 | `[4B start_time] + [4B end_time]` 赛季排位与结算时效。 |

### 4.11 深海捕鱼最新官方协议契约 (Mod 217: `Mod_Fish_Base`)

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 217, Act 0** | 查询可用鱼叉数量 (`get_player_fishhook`) | 空载荷 (`PacketBuilder(mod=217, act=0).build()`) | `[4B fishhook_count]` 可用免费鱼叉数量。<br>实测返回大端 32 位无符号整数。 |
| **Mod 217, Act 1** | 撒网捕鱼 (`do_fishing`) | 空载荷 (`PacketBuilder(mod=217, act=1).build()`) | 返回捕获鱼类信息与剩余鱼叉数量。<br>**强安全红线**：若 `fishhook_count <= 0` 必须强行中断阻断，严禁调用任何元宝购叉接口！ |

### 4.12 六道轮回塔与封灵石最新官方协议契约 (Mod 32: `Mod_Tower_Base` & Mod 100)

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 32, Act 0** | 查询轮回塔面板 (`get_tower_info`) | 空载荷 (`PacketBuilder(mod=32, act=0).build()`) | `13 字节` 定长面板结构：<br>`[1B layer, 1B cur_seq, 1B max_seq, 1B reset_cnt, 1B buy_cnt, 2B cd, 1B auto, 4B auto_time, 1B lock]`。<br>实测精准解析当前通关进度、免费重置次数与冷却时间。 |
| **Mod 100, Act 21** | 封灵石配额与领取 (`get_stone`) | 空载荷 (`PacketBuilder(mod=100, act=21).build()`) | `8 字节` 定长结构：<br>`[2B count, 2B free_quota, 2B used_quota, 2B max_quota]`。<br>实机验证稳定同步灵石配额与库存。 |
| **Mod 32, Act 7** | 快速自动爬塔 (`quickly_auto_challenge`) | `[4B start_seq, 4B stop_seq]` | 自动挑战指定区间关卡。<br>**强安全红线**：严禁元宝重置次数，严禁元宝秒 CD。 |
| **Mod 32, Act 10** | 选择挑战层数 (`select_layer`) | `[4B layer]` (如 1=修罗道, 2=地狱道等) | 切换六道塔当前挑战道法层数。 |

### 4.13 帮派进阶与吉星掷骰/七星封魔最新官方协议契约 (Mod 10: `Mod_Faction_Base`)

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与安全红线 (Response & Safety) |
| :--- | :--- | :--- | :--- |
| **Mod 10, Act 44** | 查询帮派博饼/掷骰可用次数 (`faction_roll_cake_remain_times`) | 空载荷 (`PacketBuilder(mod=10, act=44).build()`) | `[1B remain_times]` 剩余免费掷骰次数。 |
| **Mod 10, Act 46** | 帮派吉星掷骰 (`roll_cake`) | 空载荷 (`PacketBuilder(mod=10, act=46).build()`) | `19 字节` 载荷结构：<br>`[1B result (0x20=SUCCESS)] + [6B dice_points (如 04 02 01 05 06 01)] + [4B score] + [剩余字段含更新后次数]`。<br>实测零延迟稳定下发。 |
| **Mod 10, Act 45** | 帮派吉星面板与排行 (`faction_roll_cake_info`) | 空载荷 | 获取帮派内博饼积分榜与奖励配置。 |
| **Mod 10, Act 32** | 七星封魔面板与队伍状态 (`seal_satan_info`) | 空载荷 | `10 字节` 结构：`[2B monster_id, 2B hp, 2B max_hp, 2B count, 2B rank]`。 |
| **Mod 10, Act 28** | 加入/发起七星封魔 (`join_seal_satan`) | 空载荷 | 参与帮派封魔试炼，获取声望与帮贡。 |
| **Mod 0, Act 22** | 每日阵营俸禄领取 (`player_get_player_camp_salary`) | 空载荷 | `[4B salary]` 阵营俸禄铜钱。 |

---

## 5. 逆向工程扩展索引 (待办与进阶玩法)

后续扩展新任务时，需对接的已知 Mod/Act 规约：

- **神秘商人与黑市兑换**：探查城池神秘商人刷新与材料兑换；
- **生肖试炼与十二宫**：生肖挑战与境界试炼；
- **仙道会与跨服争霸**：跨服天梯赛与下注机制。

# 神仙道无头协议二进制封包规约速查矩阵 (Protocol & Action Matrix)

本文档系统汇总了神仙道微端客户端核心二进制业务协议，基于官方反编译字典库 (`data/protocol_manifest.db`) 全量校准，明确各业务功能模块号 (Mod)、动作号 (Act)、大端序封包结构契约与零元宝安全防御准则。

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
- **Payload**：业务有效载荷。若包体前两字节命中 RFC 1950 zlib 签名（`0x78` 配合 `0x01`/`0x5E`/`0x9C`/`0xDA`），由 `FrameFSM` 状态机执行流式解压。

---

## 2. 核心基础设施协议

### 2.1 登录握手与凭据校验 (Mod 0: `Mod_Player_Base`)

| 动作指令 (Act) | 十进制 / 十六进制 | 对应方法名 | 请求体字段结构 (Request Payload) | 回包字段结构 (Response Payload) |
| :--- | :--- | :--- | :--- | :--- |
| **Act 0** | `0 / 0x0000` | `login` | `write_utf(username)`<br>`write_utf(hash_token)`<br>`write_int32(server_id)`<br>`write_utf(client_version)` ... | `read_uint8(status)` (0:成功, 1:密码错, 2:封号)<br>`read_int32(player_id)`<br>`read_utf(nickname)` ... |
| **Act 72** | `72 / 0x0048` | `get_player_mission_loading_interface_id` | 空入参 | 服务端确认包 (状态同步) |
| **Act 99** | `99 / 0x0063` | `jiekou_test` | 空入参 | 版本与接口匹配回执 |
| **Act 2** | `2 / 0x0002` | `get_player_info` | 空入参 | `read_utf(name)`<br>`read_int32(player_id)`<br>`read_int32(level)`<br>`read_int64(coins)`<br>`read_int64(ingots)` ... |

### 2.2 传输层高频活性心跳保活 (Mod 0: `Mod_Player_Base`)

| 动作指令 (Act) | 十进制 / 十六进制 | 对应方法名 | 请求体字段结构 | 周期与超时规则 |
| :--- | :--- | :--- | :--- | :--- |
| **Act 75** | `75 / 0x004B` | `heart` | 空载荷 (仅 4 字节长度头 + Mod 0 + Act 75) | 推荐间隔 **3.0 秒**。服务端返回 1 字节状态位 (`ByteUtil`)。 |

---

## 3. 日常福利与资源运转协议矩阵

### 3.1 招财神符 / 摇钱树 (Mod 13: `Mod_Farm_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 12** | 查询招财神符/摇钱树状态 (`buy_coin_tree_count_info`) | 空 | 返回包含剩余免费次数、下次所需元宝等 4 项整数。 |
| **Act 13** | 摇钱招财 (`buy_coin_tree_count`) | 空 | **安全红线**：仅当免费次数 `> 0` 时方可发送；严禁在需扣除元宝时调用。 |

### 3.2 帮派祭神 (Mod 41: `Mod_WorshipMars_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询神像状态 (`mars_info`) | 空 | 返回 `[god_level, ..., free_times, max_times]`。 |
| **Act 1** | 祭神上香 (`incense`) | `write_int32(incense_type)`<br>`1: 白檀香 (消耗微量铜钱/阅历, 零元宝)`<br>`2: 苏合香 (元宝, 坚决禁止)`<br>`3: 天木香 (元宝, 坚决禁止)` | **安全红线**：仅当 `free_times > 0` 且上香参数严格为 `1` (白檀香)；若免费次数归零立即触发零元宝熔断并跳过。 |
| **Act 4** | 查询今日剩余上香次数 (`get_remain_incense_times`) | 空 | 返回今日剩余可用上香次数。 |

### 3.3 猎命系统 (Mod 22: `Mod_Fate_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询猎命师状态 (`get_fate_npc`) | 空 | 返回 5 位猎命师点亮状态。 |
| **Act 1** | 获取临时猎命槽命格 (`get_temp_fate`) | 空 | 返回待整理的命格列表。 |
| **Act 3** | 一键变卖厄运灰命 (`sale_temp_fate`) | 空或指定命格 ID 数组 | 自动将临时槽中的灰色厄运命格转化为铜钱，释放格子。 |
| **Act 2** | 一键拾取有益命格 (`pickup_fate`) | 指定命格 ID 数组 | 自动将高阶命格拾取进角色命格背包。 |
| **Act 4** | 获取正式命格背包列表 (`get_bag_list`) | 空 | 同步正式背包格子占用情况。 |

### 3.4 仙府药园 (Mod 13: `Mod_Farm_Base`)

| 模块与动作指令 | 说明 | 官方请求载荷契约 | 官方回包契约与安全红线 |
| :--- | :--- | :--- | :--- |
| **Mod 13, Act 21** | 获取已开垦土地列表 (`get_new_farmlandinfo_list`) | 空载荷 | 返回土地数组：`[4B farmland_id, 4B herbs_id, 4B farmland_time, 1B level, 1B is_plant...]`。 |
| **Mod 13, Act 22** | 获取可用仙草种子列表 (`new_farmland_herbs_list`) | 空载荷 | 返回种子列表，优先播种经验草或铜钱草。 |
| **Mod 13, Act 24** | 土地播种仙草 (`plant_new_herbs`) | `write_int32(farmland_id)`<br>`write_int32(seed_id)` | 回包状态码 `0` 或 `8` 表示成功。 |
| **Mod 13, Act 25** | 成熟仙草单倍收获 (`harvest_new`) | `write_int32(farmland_id)` | 结算大量经验与铜钱。**严禁元宝催熟或双倍**。 |
| **Mod 13, Act 19** | 探查每日仙令礼包 (`is_player_get_xian_ling_gift`) | 空载荷 | `1B Byte`：非 0 表示有未领取的仙令福利。 |
| **Mod 13, Act 20** | 领取每日仙令礼包 (`player_get_xian_ling_gift`) | 空载荷 | 成功领取仙令免费礼包。 |

### 3.5 齐天大圣摘仙桃与神龙拜祭 (Mod 40 & Mod 48)

| 模块与动作 | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Mod 40, Act 3** | 查询仙桃树状态 (`peach_info`) | 空 | 返回仙桃成熟度与轮次标识。 |
| **Mod 40, Act 4** | 查询角色偷桃进度 (`player_info`) | 空 | 返回角色当前桃树层级与待摘仙桃总数。 |
| **Mod 40, Act 5** | 一键批量摘仙桃 (`batch_get_peach`) | 空 | 结算所有待摘仙桃，获取海量升级经验，严格零元宝。 |
| **Mod 40, Act 6** | 召唤/结算白猿仙桃 (`call_peach`) | 空 | 结算白猿赠送仙桃。 |
| **Mod 48, Act 0** | 查询神兽神龙状态 (`pet_animal_info`) | 空 | 返回神龙抚养与成长状态。 |
| **Mod 48, Act 2** | 免费神龙培养喂养 (`feed_pet_animal`) | 空 | 每日免费抚养提升帮派活跃度与全队属性。 |

### 3.6 七日登录与常规每日签到 (Mod 89 & Mod 92)

| 模块与动作 | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Mod 89, Act 0** | 查询常规每日签到 (`get_sign_in_info`) | 空 (0 字节) | 返回已签到天数与今日签到状态。 |
| **Mod 89, Act 2** | 执行常规签到 (`player_sign_in`) | 空 (0 字节) | 领取今日签到铜钱、声望与道具。 |
| **Mod 92, Act 0** | 查询七日签到礼包 (`get_player_sign_in_info_two`) | 空 (0 字节) | 返回七日各阶段礼包解锁与领取状态。 |
| **Mod 92, Act 2** | 领取七日签到礼包 (`player_sign_in_two`) | 空 (0 字节) | 领取今日七日目标礼包。 |

### 3.7 在线时长礼包、微端专享礼包与阵营俸禄 (Mod 0: `Mod_Player_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Mod 0, Act 56** | 领取微端专享礼包 (`receive_client_gift`) | 空 | 每日一次，微端登录专属福利，获得铜钱、体力与阅历。 |
| **Mod 0, Act 30** | 领取在线时长礼包 (`player_get_online_gift`) | 空 | 累积在线达到档位时领取免费材料礼包。 |
| **Mod 0, Act 20** | 领取阵营每日俸禄 (`get_player_camp_salary`) | 空 | 每日一次，按角色等级与官职结算海量铜钱俸禄。 |

### 3.8 仙履奇缘 (Mod 21: `Mod_TravelEvent_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询奇遇状态 (`get_activity_info`) | 空 | 返回今日剩余答题次数（每日上限 10 次）。 |
| **Act 1** | 获取奇遇问答题目 (`get_event_and_answer`) | 空 | 返回事件题目与候选选项 A / B。 |
| **Act 2** | 提交最优答案 (`answer_travel_event`) | `write_int32(event_id)`<br>`write_int32(answer_index)` | 收益优先级策略：**体力 > 声望 > 经验 > 铜钱**。严禁元宝清 CD。 |

### 3.9 西天取经 (Mod 30: `Mod_TakeBible_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 打开取经大厅 (`open_take_bible`) | 空 | 初始化取经面板与实时护送队伍。 |
| **Act 2** | 获取角色取经状态 (`get_take_bible_info`) | 空 | 返回剩余护送次数、使者类型与刷新状态。 |
| **Act 10** | 启程西行取经 (`start_take_bible`) | 空 | 开启免费护送航程。**强安全红线**：严禁元宝加速与召唤如来。 |

### 3.10 喜从天降与通商 (Mod 757: `Mod_Traders_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 1** | 查询通商主面板 (`get_panel_info`) | 空 | 同步各大港口货物价格、代币资产与仓位上限。 |
| **Act 2** | 查询日常通商标志 (`daily_and_term_flag`) | 空 | 同步每日通商可用状态与赛季旗标。 |
| **Act 5** | 同步最新行情走势 (`latest_trend`) | `write_int32(trend_id)` | 查询当前市场物价涨跌指数与风向标。 |
| **Act 6** | 赛季窗口与排行榜 (`term_rank`) | 空 | 同步赛季结算窗口与排名。 |

### 3.11 仙女献舞 / 共舞 (Mod 76: `Mod_Dance_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询献舞状态 (`get_dance_info`) | 空 | 返回今日献舞状态与剩余次数。 |
| **Act 1** | 开启共舞 (`start_dance`) | 空 | 进入共舞挂机增益状态。 |
| **Act 2** | 领取共舞奖励 (`receive_award`) | 空 | 结算共舞累计完成的声望与经验奖励。 |

### 3.12 深海捕鱼 (Mod 217: `Mod_Fish_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 查询可用鱼叉数量 (`get_player_fishhook`) | 空 | 返回可用免费鱼叉数量 (`IntUtil`)。 |
| **Act 1** | 撒网捕鱼 (`do_fishing`) | 空 | **强安全红线**：仅当鱼叉数 `> 0` 时调用，严禁调用元宝购叉接口。 |

### 3.13 帮派吉星与七星封魔 (Mod 10: `Mod_Faction_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 44** | 查询帮派吉星剩余投掷次数 (`faction_roll_cake_remain_times`) | 空 | 返回今日剩余免费投掷次数。 |
| **Act 46** | 帮派吉星投掷 (`roll_cake`) | 空 | 投掷骰子并累加帮派积分与排行，零元宝。 |
| **Act 45** | 帮派吉星积分面板 (`faction_roll_cake_info`) | 空 | 同步帮派内博饼积分榜。 |
| **Act 32** | 七星封魔队伍状态 (`seal_satan_info`) | 空 | 查询魔头血量与当前队伍状态。 |
| **Act 28** | 加入七星封魔试炼 (`join_seal_satan`) | 空 | 参与帮派封魔，获取声望与帮贡。 |

### 3.14 背包智能规整与杂物变卖 (Mod 2: `Mod_Item_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 41** | 获取主背包物品列表 (`get_player_pack_item_list`) | 空 | 返回背包格子占用、装备与材料详情。 |
| **Act 54** | 一键自动规整背包 (`classify_pack`) | 物品列表流 | 服务端重排物品格子，消除碎片空隙。 |
| **Act 73** | 变卖低级无用杂物 (`player_sell_item`) | `write_uint16(grid_index)` | 自动变卖白色杂物换取铜钱，杜绝背包爆仓。 |

---

## 4. 战斗与副本挑战协议矩阵

### 4.1 普通副本体力极速扫荡 (Mod 25: `Mod_MissionPractice_Base`)

| 模块与动作指令 | 说明 | 官方请求载荷契约 (Request Payload) | 官方回包契约与状态定义 (Response Payload) |
| :--- | :--- | :--- | :--- |
| **Mod 25, Act 0** | 查询关卡扫荡信息 (`get_practice_info`) | `write_int32(mission_id)` | 关卡历史状态与挂机产出。 |
| **Mod 25, Act 1** | 启动全额扫荡 (`start_practice`) | `write_int32(mission_id)`<br>`write_uint16(times=0)` (0 消耗全部体力)<br>`write_uint8(auto_sale=1)` (1 开启杂物变卖) | `[1B result] + [4B remain_time] + [4B finish_time]`<br>状态码：`0`=成功, `1`=体力不足, `2`=背包已满。 |
| **Mod 25, Act 3** | 免费极速秒完成 (`quickly`) | `write_uint16(times=0)` (0 极速完成全部轮次) | 跳过倒计时，服务端即刻计算全部场次并连续推送战报与掉落。 |

### 4.2 每日精英副本扫荡 (Mod 35: `Mod_HeroMission_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 回包契约与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 获取精英副本列表 (`get_hero_mission_list`) | `write_uint16(town_id)` | 巡检该城镇内所有精英副本挑战进度与剩余次数。 |
| **Act 2** | 启动精英副本扫荡 (`start_practice`) | `write_uint16(mission_id)`<br>`write_uint8(times)`<br>`write_uint8(auto_sale)` | 发起免元宝精英扫荡。 |
| **Act 7** | 极速秒完成 (`quickly`) | 空 | 秒级完成精英副本扫荡结算。 |

### 4.3 竞技场冲榜与零元宝安全熔断 (Mod 28: `Mod_SuperSport_Base`)

| 动作指令 (Act) | 说明 | 官方请求载荷契约 | 官方回包契约与安全红线 |
| :--- | :--- | :--- | :--- |
| **Act 13** | 查询剩余免费挑战次数 (`get_challenge_times`) | 空载荷 | `[4B Int free_times]`。**若 `<= 0` 立即安全跳过，绝不付费购买额外次数**。 |
| **Act 12** | 查询挑战冷却时间 (`get_cd_time`) | 空载荷 | `[4B Int cd_time]`。若 `cd_time > 0` 安全跳过，坚决不花元宝秒 CD。 |
| **Act 1** | 拉取候选对手列表 (`get_challenge_list`) | 空载荷 | 返回候选挑战玩家列表。 |
| **Act 2** | 发起挑战 (`start_challenge`) | `write_int32(target_player_id)` | 即时战斗结算并下发声望奖励。 |

### 4.4 多人副本限时挑战 (Mod 14: `Mod_MultipleMission_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 时段门槛与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 0** | 打开多人副本面板 (`open_multiple_mission`) | 空 | 每日 **12:30-13:30** 与 **18:30-19:30** 开放，非时段前置跳过。 |
| **Act 1** | 获取队伍列表 (`get_multiple_mission_team_list`) | `write_int32(mission_id)`<br>`write_uint8(type)` | 查询现有队伍。 |
| **Act 5** | 加入队伍 (`join_multiple_mission_team`) | `write_int32(team_id)` | 加入已有房间。 |
| **Act 3** | 创建队伍 (`create_multiple_mission_team`) | `write_int32(mission_id)`<br>`write_uint8(type)` | 若无队伍自建房间。 |

### 4.5 世界 Boss 挑战与鼓舞 (Mod 24: `Mod_WorldBoss_Base`)

| 动作指令 (Act) | 说明 | 请求载荷契约 | 时段门槛与安全准则 |
| :--- | :--- | :--- | :--- |
| **Act 1** | 查询世界 Boss 数据 (`get_world_boss_data`) | 空 | 每日 **10:00** 与 **15:30** 开放。 |
| **Act 7** | 战力鼓舞 (`strengthen_combat`) | `write_uint8(type=1)` (1: 阅历鼓舞) | **强安全红线**：入参严格硬编码为 `1` (阅历)，严禁使用元宝鼓舞。 |
| **Act 2** | 发起挑战 (`fight_world_boss`) | `write_uint8(boss_type)` | 挑战巨兽，即时结算伤害与声望。 |
| **Act 3** | 清除阵亡冷却复活 (`clear_death_cd`) | 空 | 免费复活或等待冷却计时，坚决不扣元宝秒复活。 |

### 4.6 六道轮回塔与封灵石 (Mod 32: `Mod_Tower_Base` & Mod 100)

| 模块与动作指令 | 说明 | 官方请求载荷契约 | 官方回包契约与安全红线 |
| :--- | :--- | :--- | :--- |
| **Mod 32, Act 0** | 查询轮回塔面板 (`get_tower_info`) | 空载荷 | 定长面板结构：当前层、关卡进度、免费重置次数与冷却。 |
| **Mod 32, Act 7** | 快速自动爬塔 (`quickly_auto_challenge`) | `[1B start_seq, 1B stop_seq]` | 自动挑战指定关卡。严禁元宝重置次数。 |
| **Mod 100, Act 19** | 领取封灵石配额 (`get_stone`) | 空载荷 | 每日免费领取封灵石材料。 |

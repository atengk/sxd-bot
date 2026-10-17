# Notify 模块协议规约 (Mod 20)

> **模块编号**：`20`  
> **官方类名**：`com.protocols::Mod_Notify_Base`  
> **动作总数**：`108` 个  
> **常量总数**：`36` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `BACK_LOTTERY` | `27` | 业务状态或错误枚举码 |
| `CHANGE_MONEY` | `6` | 业务状态或错误枚举码 |
| `CHRISTMAS_SEND_GIFT` | `35` | 业务状态或错误枚举码 |
| `CLOSE` | `20` | 业务状态或错误枚举码 |
| `COIN` | `14` | 业务状态或错误枚举码 |
| `COINS` | `0` | 业务状态或错误枚举码 |
| `DOUBLE_TURNTABLE` | `32` | 业务状态或错误枚举码 |
| `DRAGONBALL_SACRIFICE` | `17` | 业务状态或错误枚举码 |
| `DRAGONBALL_WISH` | `18` | 业务状态或错误枚举码 |
| `DUN_HUANG` | `31` | 业务状态或错误枚举码 |
| `EXPLORE_FORBIDDEN` | `22` | 业务状态或错误枚举码 |
| `FACTION` | `5` | 业务状态或错误枚举码 |
| `FAME` | `3` | 业务状态或错误枚举码 |
| `FATE` | `15` | 业务状态或错误枚举码 |
| `GOLD_TOWER` | `34` | 业务状态或错误枚举码 |
| `ITEM` | `1` | 业务状态或错误枚举码 |
| `ITEM_DECIPHER` | `7` | 业务状态或错误枚举码 |
| `LONG_GONG` | `29` | 业务状态或错误枚举码 |
| `MAKE_SKILL_BOOK` | `21` | 业务状态或错误枚举码 |
| `MEMENTO_COIN_EXCHANGE` | `28` | 业务状态或错误枚举码 |
| `MOONLIGHT_BOX` | `33` | 业务状态或错误枚举码 |
| `MYSTIC_CAPURE` | `8` | 业务状态或错误枚举码 |
| `NINE_DOOR` | `30` | 业务状态或错误枚举码 |
| `OPEN` | `19` | 业务状态或错误枚举码 |
| `PARADE_START` | `25` | 业务状态或错误枚举码 |
| `READY_WEDDING` | `23` | 业务状态或错误枚举码 |
| `ROLE` | `2` | 业务状态或错误枚举码 |
| `RULAI_CLOSE` | `10` | 业务状态或错误枚举码 |
| `RULAI_OPEN` | `11` | 业务状态或错误枚举码 |
| `RULAI_OPEN_FOR_CALL` | `9` | 业务状态或错误枚举码 |
| `STATEPOINT` | `13` | 业务状态或错误枚举码 |
| `STATE_POINT_LV` | `12` | 业务状态或错误枚举码 |
| `TANG_SENG` | `4` | 业务状态或错误枚举码 |
| `WEDDING_END` | `26` | 业务状态或错误枚举码 |
| `WEDDING_START` | `24` | 业务状态或错误枚举码 |
| `XIANLING` | `16` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `mission_award` (Action 0)

- **模块与动作标识**：`Mod = 20`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.2 `pk_award` (Action 1)

- **模块与动作标识**：`Mod = 20`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.3 `complete_reel_production` (Action 2)

- **模块与动作标识**：`Mod = 20`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.11 `role_num_notify` (Action 10)

- **模块与动作标识**：`Mod = 20`, `Act = 10`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.12 `new_research_notify` (Action 11)

- **模块与动作标识**：`Mod = 20`, `Act = 11`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, str]` | 网络大端序编解码 |

### 2.13 `new_partners_notify` (Action 12)

- **模块与动作标识**：`Mod = 20`, `Act = 12`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.14 `notify_get_good_fate` (Action 13)

- **模块与动作标识**：`Mod = 20`, `Act = 13`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.15 `notify_player_mission_practice_status` (Action 14)

- **模块与动作标识**：`Mod = 20`, `Act = 14`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.16 `update_player_super_gift` (Action 15)

- **模块与动作标识**：`Mod = 20`, `Act = 15`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(4)` | `Tuple[int, int, int, str]` | 网络大端序编解码 |

### 2.17 `change_equip` (Action 16)

- **模块与动作标识**：`Mod = 20`, `Act = 16`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.18 `update_lucky_shop_item` (Action 17)

- **模块与动作标识**：`Mod = 20`, `Act = 17`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.19 `buy_good_stuff_in_lucky_shop` (Action 18)

- **模块与动作标识**：`Mod = 20`, `Act = 18`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.20 `disband_faction_notify` (Action 19)

- **模块与动作标识**：`Mod = 20`, `Act = 19`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.21 `kickout_member_notify` (Action 20)

- **模块与动作标识**：`Mod = 20`, `Act = 20`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.23 `player_take_bible` (Action 22)

- **模块与动作标识**：`Mod = 20`, `Act = 22`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.24 `player_take_bible_berobbed` (Action 23)

- **模块与动作标识**：`Mod = 20`, `Act = 23`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.25 `game_timer` (Action 24)

- **模块与动作标识**：`Mod = 20`, `Act = 24`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.26 `send_flower` (Action 25)

- **模块与动作标识**：`Mod = 20`, `Act = 25`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.27 `pass_tower` (Action 26)

- **模块与动作标识**：`Mod = 20`, `Act = 26`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.29 `update_rulai_status` (Action 28)

- **模块与动作标识**：`Mod = 20`, `Act = 28`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, str]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.30 `roll_cake` (Action 29)

- **模块与动作标识**：`Mod = 20`, `Act = 29`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.31 `update_server_war_step` (Action 30)

- **模块与动作标识**：`Mod = 20`, `Act = 30`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.32 `have_new_server_war_report` (Action 31)

- **模块与动作标识**：`Mod = 20`, `Act = 31`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.33 `server_war_winner` (Action 32)

- **模块与动作标识**：`Mod = 20`, `Act = 32`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.34 `world_war_top_login` (Action 33)

- **模块与动作标识**：`Mod = 20`, `Act = 33`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.35 `zodiac_entry_notify` (Action 34)

- **模块与动作标识**：`Mod = 20`, `Act = 34`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.36 `get_pet_animal_exp` (Action 35)

- **模块与动作标识**：`Mod = 20`, `Act = 35`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.37 `study_stunt_notify` (Action 36)

- **模块与动作标识**：`Mod = 20`, `Act = 36`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.38 `flower_week_number_one` (Action 37)

- **模块与动作标识**：`Mod = 20`, `Act = 37`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.39 `cat_hunt_golden_box` (Action 38)

- **模块与动作标识**：`Mod = 20`, `Act = 38`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.40 `update_world_faction_war_step` (Action 39)

- **模块与动作标识**：`Mod = 20`, `Act = 39`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.41 `update_world_faction_war_team` (Action 40)

- **模块与动作标识**：`Mod = 20`, `Act = 40`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.42 `world_faction_war_winner` (Action 41)

- **模块与动作标识**：`Mod = 20`, `Act = 41`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.43 `have_new_world_faction_war_report` (Action 42)

- **模块与动作标识**：`Mod = 20`, `Act = 42`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.44 `week_ranking` (Action 43)

- **模块与动作标识**：`Mod = 20`, `Act = 43`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.45 `special_notify` (Action 44)

- **模块与动作标识**：`Mod = 20`, `Act = 44`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.46 `find_immortal_five_notify` (Action 45)

- **模块与动作标识**：`Mod = 20`, `Act = 45`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.48 `unlock_special_partner` (Action 47)

- **模块与动作标识**：`Mod = 20`, `Act = 47`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

### 2.49 `world_top_war_gift_has_white_tiger` (Action 48)

- **模块与动作标识**：`Mod = 20`, `Act = 48`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.50 `lucky_wheel_award_seven_medicine_reel` (Action 49)

- **模块与动作标识**：`Mod = 20`, `Act = 49`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.51 `update_server_faction_war_step` (Action 50)

- **模块与动作标识**：`Mod = 20`, `Act = 50`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.52 `have_new_server_faction_war_report` (Action 51)

- **模块与动作标识**：`Mod = 20`, `Act = 51`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.53 `server_faction_war_winner` (Action 52)

- **模块与动作标识**：`Mod = 20`, `Act = 52`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.54 `ingot_luck_wheel_notify` (Action 53)

- **模块与动作标识**：`Mod = 20`, `Act = 53`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.55 `study_sigil_stunt_notify` (Action 54)

- **模块与动作标识**：`Mod = 20`, `Act = 54`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.56 `get_good_fate_notify` (Action 55)

- **模块与动作标识**：`Mod = 20`, `Act = 55`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.57 `notify_unlock_excl_arti` (Action 56)

- **模块与动作标识**：`Mod = 20`, `Act = 56`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.58 `notify_christmas_activity_award` (Action 57)

- **模块与动作标识**：`Mod = 20`, `Act = 57`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.59 `notify_player_change_job` (Action 58)

- **模块与动作标识**：`Mod = 20`, `Act = 58`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.60 `notify_lantern_festival_award` (Action 59)

- **模块与动作标识**：`Mod = 20`, `Act = 59`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.61 `notify_player_hunt_demon_award` (Action 60)

- **模块与动作标识**：`Mod = 20`, `Act = 60`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.62 `update_twin_dragons_step` (Action 61)

- **模块与动作标识**：`Mod = 20`, `Act = 61`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.63 `have_new_twin_dragons_report` (Action 62)

- **模块与动作标识**：`Mod = 20`, `Act = 62`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.64 `twin_dragons_winner` (Action 63)

- **模块与动作标识**：`Mod = 20`, `Act = 63`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.65 `open_st_boss_gift_notify` (Action 64)

- **模块与动作标识**：`Mod = 20`, `Act = 64`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.66 `notify_unlock_supernatural` (Action 65)

- **模块与动作标识**：`Mod = 20`, `Act = 65`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.67 `study_exclusive_supernatural_notify` (Action 66)

- **模块与动作标识**：`Mod = 20`, `Act = 66`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.68 `have_new_new_top_war_report` (Action 67)

- **模块与动作标识**：`Mod = 20`, `Act = 67`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.69 `new_top_war_winner` (Action 68)

- **模块与动作标识**：`Mod = 20`, `Act = 68`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.70 `circle_war_notify` (Action 69)

- **模块与动作标识**：`Mod = 20`, `Act = 69`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.71 `sacrifice_dragonball_notify` (Action 70)

- **模块与动作标识**：`Mod = 20`, `Act = 70`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.72 `sacrifice_dragonball_world_channel_notify` (Action 71)

- **模块与动作标识**：`Mod = 20`, `Act = 71`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.73 `gamable_level_1_notify` (Action 72)

- **模块与动作标识**：`Mod = 20`, `Act = 72`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.74 `gamable_result_notify` (Action 73)

- **模块与动作标识**：`Mod = 20`, `Act = 73`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.75 `player_st_take_bible` (Action 74)

- **模块与动作标识**：`Mod = 20`, `Act = 74`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.76 `player_st_take_bible_berobbed` (Action 75)

- **模块与动作标识**：`Mod = 20`, `Act = 75`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_6` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.77 `update_st_sup_war_step` (Action 76)

- **模块与动作标识**：`Mod = 20`, `Act = 76`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.78 `have_new_st_sup_war_report` (Action 77)

- **模块与动作标识**：`Mod = 20`, `Act = 77`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.79 `st_sup_war_winner` (Action 78)

- **模块与动作标识**：`Mod = 20`, `Act = 78`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.80 `notify_luxury_seat` (Action 79)

- **模块与动作标识**：`Mod = 20`, `Act = 79`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.81 `have_new_god_war_report` (Action 80)

- **模块与动作标识**：`Mod = 20`, `Act = 80`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.82 `god_war_winner` (Action 81)

- **模块与动作标识**：`Mod = 20`, `Act = 81`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.83 `sky_lantern_bless_gold_quality` (Action 82)

- **模块与动作标识**：`Mod = 20`, `Act = 82`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.84 `war_power_change` (Action 83)

- **模块与动作标识**：`Mod = 20`, `Act = 83`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `LongUtil` | `int` | 网络大端序编解码 |

### 2.85 `sky_lantern_bless_top_one` (Action 84)

- **模块与动作标识**：`Mod = 20`, `Act = 84`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.86 `make_chaos_item` (Action 85)

- **模块与动作标识**：`Mod = 20`, `Act = 85`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.87 `notify_travel_shop_status` (Action 86)

- **模块与动作标识**：`Mod = 20`, `Act = 86`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.88 `notify_player_new_gift` (Action 87)

- **模块与动作标识**：`Mod = 20`, `Act = 87`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.89 `christmas_hunt_demon_notify` (Action 88)

- **模块与动作标识**：`Mod = 20`, `Act = 88`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.90 `become_immortal` (Action 89)

- **模块与动作标识**：`Mod = 20`, `Act = 89`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.91 `notify_st_boss_detect_title` (Action 90)

- **模块与动作标识**：`Mod = 20`, `Act = 90`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.92 `lotus_lamp_colorful_quality` (Action 91)

- **模块与动作标识**：`Mod = 20`, `Act = 91`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.93 `wish_tree_good_quality` (Action 92)

- **模块与动作标识**：`Mod = 20`, `Act = 92`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.94 `notify_card_master_draw` (Action 93)

- **模块与动作标识**：`Mod = 20`, `Act = 93`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.95 `super_prize_pool_notify` (Action 94)

- **模块与动作标识**：`Mod = 20`, `Act = 94`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.96 `awake_skill_book_notify` (Action 95)

- **模块与动作标识**：`Mod = 20`, `Act = 95`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.97 `firework_notify` (Action 96)

- **模块与动作标识**：`Mod = 20`, `Act = 96`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.98 `marry_notify` (Action 97)

- **模块与动作标识**：`Mod = 20`, `Act = 97`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.99 `change_notify` (Action 98)

- **模块与动作标识**：`Mod = 20`, `Act = 98`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.100 `lottery_ticket_winner_notify` (Action 99)

- **模块与动作标识**：`Mod = 20`, `Act = 99`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.101 `five_blessings_notify` (Action 100)

- **模块与动作标识**：`Mod = 20`, `Act = 100`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.102 `four_anniversary_back_lottery_notify` (Action 101)

- **模块与动作标识**：`Mod = 20`, `Act = 101`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.103 `update_st_arena_step` (Action 102)

- **模块与动作标识**：`Mod = 20`, `Act = 102`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.104 `st_indiana_jones_box_award` (Action 103)

- **模块与动作标识**：`Mod = 20`, `Act = 103`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.105 `world_sky_lantern_bless_gold_quality` (Action 104)

- **模块与动作标识**：`Mod = 20`, `Act = 104`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.106 `update_st_union_sixvsix_step` (Action 105)

- **模块与动作标识**：`Mod = 20`, `Act = 105`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.107 `have_new_st_union_sixvsix_report` (Action 106)

- **模块与动作标识**：`Mod = 20`, `Act = 106`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.108 `st_union_sixvsix_winner` (Action 107)

- **模块与动作标识**：`Mod = 20`, `Act = 107`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.109 `hide_treasure_map_item` (Action 108)

- **模块与动作标识**：`Mod = 20`, `Act = 108`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.110 `player_sa_take_bible` (Action 109)

- **模块与动作标识**：`Mod = 20`, `Act = 109`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.111 `player_sa_take_bible_berobbed` (Action 110)

- **模块与动作标识**：`Mod = 20`, `Act = 110`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.112 `notify_sa_luxury_seat` (Action 111)

- **模块与动作标识**：`Mod = 20`, `Act = 111`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.113 `notify_activity_award` (Action 112)

- **模块与动作标识**：`Mod = 20`, `Act = 112`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.114 `update_new_server_war_step` (Action 113)

- **模块与动作标识**：`Mod = 20`, `Act = 113`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.115 `new_have_new_server_war_report` (Action 114)

- **模块与动作标识**：`Mod = 20`, `Act = 114`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.116 `zongzi_vote_camp_vote` (Action 115)

- **模块与动作标识**：`Mod = 20`, `Act = 115`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.117 `notify_player_charge` (Action 116)

- **模块与动作标识**：`Mod = 20`, `Act = 116`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.118 `fairy_game_notify` (Action 117)

- **模块与动作标识**：`Mod = 20`, `Act = 117`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_20_notify import (
    NotifyMissionAwardReq,
    NotifyMissionAwardResp,
)

# 发起 Mod 20 业务请求
```

# Farm 模块协议规约 (Mod 13)

> **模块编号**：`13`  
> **官方类名**：`com.protocols::Mod_Farm_Base`  
> **动作总数**：`27` 个  
> **常量总数**：`35` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `CAN_NOT_UP` | `29` | 业务状态或错误枚举码 |
| `COIN_HERBS` | `3` | 业务状态或错误枚举码 |
| `ERROR` | `33` | 业务状态或错误枚举码 |
| `EXP_HERBS` | `2` | 业务状态或错误枚举码 |
| `FAILED` | `30` | 业务状态或错误枚举码 |
| `INVITE` | `6` | 业务状态或错误枚举码 |
| `IS_DOUBLE` | `14` | 业务状态或错误枚举码 |
| `IS_MAIN_ROLE` | `19` | 业务状态或错误枚举码 |
| `IS_PLANT` | `28` | 业务状态或错误枚举码 |
| `IS_TOP_HERBS` | `11` | 业务状态或错误枚举码 |
| `ITEM_PACK_FULL` | `34` | 业务状态或错误枚举码 |
| `LIMIT_NUM` | `25` | 业务状态或错误枚举码 |
| `NOINVITE` | `7` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `10` | 业务状态或错误枚举码 |
| `NOT_ENOUGTH_COIN` | `31` | 业务状态或错误枚举码 |
| `NOT_ENOUGTH_INGOT` | `32` | 业务状态或错误枚举码 |
| `NOT_PLAYER_ROLE` | `18` | 业务状态或错误枚举码 |
| `NO_DOUBLE` | `15` | 业务状态或错误枚举码 |
| `NO_ENOUGHT_COIN_TREE_COUNT` | `12` | 业务状态或错误枚举码 |
| `NO_ENOUGHT_XIANLING_TREE_COUNT` | `13` | 业务状态或错误枚举码 |
| `NO_ENOUGTH_TIMES` | `26` | 业务状态或错误枚举码 |
| `NO_INGOT` | `24` | 业务状态或错误枚举码 |
| `NO_PLANT` | `1` | 业务状态或错误枚举码 |
| `NO_REMAIN` | `23` | 业务状态或错误枚举码 |
| `NO_VIP` | `27` | 业务状态或错误枚举码 |
| `PACK_FULL` | `16` | 业务状态或错误枚举码 |
| `PASS` | `21` | 业务状态或错误枚举码 |
| `PLANT` | `0` | 业务状态或错误枚举码 |
| `REACH_MAX_LAND_COUNT` | `17` | 业务状态或错误枚举码 |
| `REMAIN` | `22` | 业务状态或错误枚举码 |
| `ROLE_LEVEL` | `20` | 业务状态或错误枚举码 |
| `SUCCESS` | `8` | 业务状态或错误枚举码 |
| `TOP_HERBS` | `9` | 业务状态或错误枚举码 |
| `WAR` | `5` | 业务状态或错误枚举码 |
| `XIANLING_HERBS` | `4` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `get_farmlandinfo_list` (Action 0)

- **模块与动作标识**：`Mod = 13`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(13)` | `Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.2 `get_player_roleinfo_list` (Action 1)

- **模块与动作标识**：`Mod = 13`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(10)` | `Tuple[int, str, str, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.3 `get_herbs_seed` (Action 2)

- **模块与动作标识**：`Mod = 13`, `Act = 2`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.4 `refresh_herbs_seed` (Action 3)

- **模块与动作标识**：`Mod = 13`, `Act = 3`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.5 `get_top_herbs_seed` (Action 4)

- **模块与动作标识**：`Mod = 13`, `Act = 4`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.6 `plant_herbs` (Action 5)

- **模块与动作标识**：`Mod = 13`, `Act = 5`
- **请求参数字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`15` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.7 `harvest` (Action 6)

- **模块与动作标识**：`Mod = 13`, `Act = 6`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.8 `reclamation` (Action 7)

- **模块与动作标识**：`Mod = 13`, `Act = 7`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.9 `check_role_state` (Action 8)

- **模块与动作标识**：`Mod = 13`, `Act = 8`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.10 `harvest_check_remain_exp` (Action 9)

- **模块与动作标识**：`Mod = 13`, `Act = 9`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.11 `get_simple_farmlandinfo` (Action 10)

- **模块与动作标识**：`Mod = 13`, `Act = 10`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.12 `clear_farmland_cd` (Action 11)

- **模块与动作标识**：`Mod = 13`, `Act = 11`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.13 `buy_coin_tree_count_info` (Action 12)

- **模块与动作标识**：`Mod = 13`, `Act = 12`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.14 `buy_coin_tree_count` (Action 13)

- **模块与动作标识**：`Mod = 13`, `Act = 13`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.15 `coin_tree_count_notify` (Action 14)

- **模块与动作标识**：`Mod = 13`, `Act = 14`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.16 `ingot_for_farmland` (Action 15)

- **模块与动作标识**：`Mod = 13`, `Act = 15`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.17 `up_farmland_level` (Action 16)

- **模块与动作标识**：`Mod = 13`, `Act = 16`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.18 `xianling_tree_count_notify` (Action 17)

- **模块与动作标识**：`Mod = 13`, `Act = 17`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.19 `xianling_tree_count_info` (Action 18)

- **模块与动作标识**：`Mod = 13`, `Act = 18`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.20 `is_player_get_xian_ling_gift` (Action 19)

- **模块与动作标识**：`Mod = 13`, `Act = 19`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.21 `player_get_xian_ling_gift` (Action 20)

- **模块与动作标识**：`Mod = 13`, `Act = 20`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.22 `get_new_farmlandinfo_list` (Action 21)

- **模块与动作标识**：`Mod = 13`, `Act = 21`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(6)` | `Tuple[int, int, int, int, int, Tuple[int, int, int]]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.23 `new_farmland_herbs_list` (Action 22)

- **模块与动作标识**：`Mod = 13`, `Act = 22`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(5)` | `Tuple[int, int, int, int, int]` | 网络大端序编解码 |

### 2.24 `buy_new_herbs` (Action 23)

- **模块与动作标识**：`Mod = 13`, `Act = 23`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.25 `plant_new_herbs` (Action 24)

- **模块与动作标识**：`Mod = 13`, `Act = 24`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.26 `harvest_new` (Action 25)

- **模块与动作标识**：`Mod = 13`, `Act = 25`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.27 `new_clear_farmland_cd` (Action 26)

- **模块与动作标识**：`Mod = 13`, `Act = 26`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_13_farm import (
    FarmGetFarmlandinfoListReq,
    FarmGetFarmlandinfoListResp,
)

# 发起 Mod 13 业务请求
```

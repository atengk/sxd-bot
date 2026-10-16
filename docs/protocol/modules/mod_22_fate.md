# Fate 模块协议规约 (Mod 22)

> **模块编号**：`22`  
> **官方类名**：`com.protocols::Mod_Fate_Base`  
> **动作总数**：`41` 个  
> **常量总数**：`44` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `BAG_FULL` | `1` | 业务状态或错误枚举码 |
| `BAG_TO_ROLE` | `17` | 业务状态或错误枚举码 |
| `CANT_MERGE` | `20` | 业务状态或错误枚举码 |
| `CANT_TAICHU_QIANLI` | `21` | 业务状态或错误枚举码 |
| `FAILD` | `43` | 业务状态或错误枚举码 |
| `FAILED` | `4` | 业务状态或错误枚举码 |
| `FALSE` | `39` | 业务状态或错误枚举码 |
| `FATE_CAN_EXCHANGE` | `25` | 业务状态或错误枚举码 |
| `FATE_CAN_PICK_UP` | `3` | 业务状态或错误枚举码 |
| `FATE_PACK_FULL` | `33` | 业务状态或错误枚举码 |
| `FULL_BUY_TIMES` | `24` | 业务状态或错误枚举码 |
| `FULL_TEMP_BAG` | `13` | 业务状态或错误枚举码 |
| `FUNCTION_NO_OPEN` | `36` | 业务状态或错误枚举码 |
| `HAVE_SAME_TYPE_FATE` | `7` | 业务状态或错误枚举码 |
| `HAVE_WEAR_ON` | `8` | 业务状态或错误枚举码 |
| `INVALID_FATE_NPC_ID` | `12` | 业务状态或错误枚举码 |
| `INVALID_GRID` | `2` | 业务状态或错误枚举码 |
| `INVALID_LEVEL` | `10` | 业务状态或错误枚举码 |
| `INVALID_NPC_ID` | `23` | 业务状态或错误枚举码 |
| `INVALID_POSITION` | `9` | 业务状态或错误枚举码 |
| `IN_BAG` | `15` | 业务状态或错误枚举码 |
| `IS_LOCKED` | `11` | 业务状态或错误枚举码 |
| `LIMILT_NUM` | `42` | 业务状态或错误枚举码 |
| `MAX_BAG_NUMBER` | `6` | 业务状态或错误枚举码 |
| `MAX_LEVEL` | `19` | 业务状态或错误枚举码 |
| `NOT_BREAKTHROUGHS` | `41` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_COIN` | `14` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_COINS` | `37` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_COUNT` | `27` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `5` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_LEVEL` | `26` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_MING_GONG` | `40` | 业务状态或错误枚举码 |
| `NO_ENOUGH_BAGS` | `30` | 业务状态或错误枚举码 |
| `NO_ENOUGH_COINS` | `31` | 业务状态或错误枚举码 |
| `NO_ENOUGH_LEVEL` | `32` | 业务状态或错误枚举码 |
| `NO_MERGE_ENOUGH_LEVEL` | `22` | 业务状态或错误枚举码 |
| `ON_ROLE` | `16` | 业务状态或错误枚举码 |
| `PLAYER_CANCEL` | `34` | 业务状态或错误枚举码 |
| `PURPLE` | `28` | 业务状态或错误枚举码 |
| `ROLE_TO_BAG` | `18` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |
| `TRUE` | `38` | 业务状态或错误枚举码 |
| `UPGRADED_ALL` | `35` | 业务状态或错误枚举码 |
| `YELLOW` | `29` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `get_fate_npc` (Action 0)

- **模块与动作标识**：`Mod = 22`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(5)` | `Tuple[int, int, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.2 `get_temp_fate` (Action 1)

- **模块与动作标识**：`Mod = 22`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.3 `pickup_fate` (Action 2)

- **模块与动作标识**：`Mod = 22`, `Act = 2`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[LongUtil]` | `List[int]` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Array[LongUtil]` | `List[int]` | 网络大端序编解码 |

### 2.4 `sale_temp_fate` (Action 3)

- **模块与动作标识**：`Mod = 22`, `Act = 3`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[LongUtil]` | `List[int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.5 `get_bag_list` (Action 4)

- **模块与动作标识**：`Mod = 22`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`11` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(11)` | `Tuple[int, int, int, int, int, int, int, int, List[int], int, int]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `Tuple(3)` | `Tuple[int, int, Tuple[int, int]]` | 网络大端序编解码 |

### 2.6 `buy_bag_grid` (Action 5)

- **模块与动作标识**：`Mod = 22`, `Act = 5`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.7 `get_role_fate_list` (Action 6)

- **模块与动作标识**：`Mod = 22`, `Act = 6`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(11)` | `Tuple[int, int, int, int, int, int, int, int, List[int], int, int]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.8 `wear_on` (Action 7)

- **模块与动作标识**：`Mod = 22`, `Act = 7`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.9 `discard_fate` (Action 8)

- **模块与动作标识**：`Mod = 22`, `Act = 8`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.10 `appoint_fate_npc` (Action 9)

- **模块与动作标识**：`Mod = 22`, `Act = 9`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `LongUtil` | `int` | 网络大端序编解码 |

### 2.11 `wear_off_fate` (Action 10)

- **模块与动作标识**：`Mod = 22`, `Act = 10`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.13 `change_fate_grid` (Action 12)

- **模块与动作标识**：`Mod = 22`, `Act = 12`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.14 `merge` (Action 13)

- **模块与动作标识**：`Mod = 22`, `Act = 13`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`12` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `Array[ShortUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.15 `change_position` (Action 14)

- **模块与动作标识**：`Mod = 22`, `Act = 14`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.16 `get_player_role_fate_power` (Action 15)

- **模块与动作标识**：`Mod = 22`, `Act = 15`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.17 `get_merge_data` (Action 16)

- **模块与动作标识**：`Mod = 22`, `Act = 16`
- **请求参数字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.18 `merge_all_in_bag` (Action 17)

- **模块与动作标识**：`Mod = 22`, `Act = 17`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.19 `buy_fate_npc` (Action 18)

- **模块与动作标识**：`Mod = 22`, `Act = 18`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.20 `exchange_fate` (Action 19)

- **模块与动作标识**：`Mod = 22`, `Act = 19`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.21 `get_scrap_amount` (Action 20)

- **模块与动作标识**：`Mod = 22`, `Act = 20`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.22 `merge_all_normal_in_bag` (Action 21)

- **模块与动作标识**：`Mod = 22`, `Act = 21`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.23 `exchange_unknow_fire` (Action 22)

- **模块与动作标识**：`Mod = 22`, `Act = 22`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.24 `get_fate_cat_skill` (Action 23)

- **模块与动作标识**：`Mod = 22`, `Act = 23`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

### 2.25 `use_fate_cat_skill` (Action 24)

- **模块与动作标识**：`Mod = 22`, `Act = 24`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.26 `crazy_fate` (Action 25)

- **模块与动作标识**：`Mod = 22`, `Act = 25`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.27 `cancel_crazy_fate` (Action 26)

- **模块与动作标识**：`Mod = 22`, `Act = 26`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.28 `notify_crazy_fate_result` (Action 27)

- **模块与动作标识**：`Mod = 22`, `Act = 27`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Array[ShortUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.29 `get_upgrade_fate_npc_id` (Action 28)

- **模块与动作标识**：`Mod = 22`, `Act = 28`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.30 `upgrade_fate_npc` (Action 29)

- **模块与动作标识**：`Mod = 22`, `Act = 29`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.31 `get_fate_inn_upgrade_flag` (Action 30)

- **模块与动作标识**：`Mod = 22`, `Act = 30`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.32 `get_ming_gong_info` (Action 31)

- **模块与动作标识**：`Mod = 22`, `Act = 31`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.33 `exchange_ming_gong` (Action 32)

- **模块与动作标识**：`Mod = 22`, `Act = 32`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.34 `breakthroughs_fate` (Action 33)

- **模块与动作标识**：`Mod = 22`, `Act = 33`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.35 `exchange_ming_gong_scrap` (Action 34)

- **模块与动作标识**：`Mod = 22`, `Act = 34`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.36 `fate_lock` (Action 35)

- **模块与动作标识**：`Mod = 22`, `Act = 35`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.37 `fate_unlock` (Action 36)

- **模块与动作标识**：`Mod = 22`, `Act = 36`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.38 `unlock_fate` (Action 37)

- **模块与动作标识**：`Mod = 22`, `Act = 37`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.39 `new_crazy_fate` (Action 38)

- **模块与动作标识**：`Mod = 22`, `Act = 38`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Array[ShortUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.40 `set_fate_merge_setting` (Action 39)

- **模块与动作标识**：`Mod = 22`, `Act = 39`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.41 `change_taichu_auto_merge_state` (Action 40)

- **模块与动作标识**：`Mod = 22`, `Act = 40`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.42 `classify_ware` (Action 41)

- **模块与动作标识**：`Mod = 22`, `Act = 41`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_22_fate import (
    FateGetFateNpcReq,
    FateGetFateNpcResp,
)

# 发起 Mod 22 业务请求
```

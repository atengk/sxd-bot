# TakeBible 模块协议规约 (Mod 30)

> **模块编号**：`30`  
> **官方类名**：`com.protocols::Mod_TakeBible_Base`  
> **动作总数**：`22` 个  
> **常量总数**：`39` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `APPLY_PROTECT` | `34` | 业务状态或错误枚举码 |
| `ARRIVAL` | `28` | 业务状态或错误枚举码 |
| `BAI_LONG_MA` | `0` | 业务状态或错误枚举码 |
| `BEROB` | `32` | 业务状态或错误枚举码 |
| `BE_MONSTER_ROB` | `31` | 业务状态或错误枚举码 |
| `BE_ROB_ALL` | `21` | 业务状态或错误枚举码 |
| `CANCEL_APPLY` | `13` | 业务状态或错误枚举码 |
| `CLOSE` | `5` | 业务状态或错误枚举码 |
| `FRIEND_APPROVE_APPLY` | `29` | 业务状态或错误枚举码 |
| `FRIEND_REJECT_APPLY` | `30` | 业务状态或错误枚举码 |
| `FULL_PROTECT_TIMES` | `10` | 业务状态或错误枚举码 |
| `FULL_ROB_TIMES` | `19` | 业务状态或错误枚举码 |
| `FULL_TAKE_BIBLE_TIMES` | `17` | 业务状态或错误枚举码 |
| `HAVE_CD_TIME` | `20` | 业务状态或错误枚举码 |
| `INVALID_PLAYER_ID` | `9` | 业务状态或错误枚举码 |
| `INVALID_TYPE` | `35` | 业务状态或错误枚举码 |
| `KILL_ALL` | `37` | 业务状态或错误枚举码 |
| `KILL_ONE` | `36` | 业务状态或错误枚举码 |
| `KILL_ONE_NO_AWARD` | `38` | 业务状态或错误枚举码 |
| `NEW_TAKE_BIBLE` | `26` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `15` | 业务状态或错误枚举码 |
| `NOT_ONLINE` | `11` | 业务状态或错误枚举码 |
| `OPEN` | `7` | 业务状态或错误枚举码 |
| `OPEN_FOR_CALL` | `6` | 业务状态或错误枚举码 |
| `PROTECT_BEROB` | `33` | 业务状态或错误枚举码 |
| `PROTECT_STATUS` | `14` | 业务状态或错误枚举码 |
| `QUICKLY` | `27` | 业务状态或错误枚举码 |
| `REQUEST_VIP` | `16` | 业务状态或错误枚举码 |
| `REROB` | `18` | 业务状态或错误枚举码 |
| `ROB` | `24` | 业务状态或错误枚举码 |
| `SHA_WU_JING` | `1` | 业务状态或错误枚举码 |
| `SUCCESS` | `8` | 业务状态或错误枚举码 |
| `SUN_WU_KONG` | `3` | 业务状态或错误枚举码 |
| `TAKE_BIBLE` | `25` | 业务状态或错误枚举码 |
| `TAKE_BIBLE_STATUS` | `12` | 业务状态或错误枚举码 |
| `TANGSENG_BE_ROB_ALL` | `23` | 业务状态或错误枚举码 |
| `TANGSENG_FULL_ROB_TIMES` | `22` | 业务状态或错误枚举码 |
| `TANG_SENG` | `4` | 业务状态或错误枚举码 |
| `ZHU_BA_JIE` | `2` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `open_take_bible` (Action 0)

- **模块与动作标识**：`Mod = 30`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(8)` | `Tuple[int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.2 `close_take_bible` (Action 1)

- **模块与动作标识**：`Mod = 30`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.3 `get_take_bible_info` (Action 2)

- **模块与动作标识**：`Mod = 30`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(4)` | `Tuple[int, int, int, int]` | 网络大端序编解码 |
  | `field_1` | `Tuple(5)` | `Tuple[int, str, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.4 `apply_friend` (Action 3)

- **模块与动作标识**：`Mod = 30`, `Act = 3`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.5 `cancel_apply_friend` (Action 4)

- **模块与动作标识**：`Mod = 30`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.6 `approve_apply` (Action 5)

- **模块与动作标识**：`Mod = 30`, `Act = 5`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.7 `reject_apply` (Action 6)

- **模块与动作标识**：`Mod = 30`, `Act = 6`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.8 `buy_protection` (Action 7)

- **模块与动作标识**：`Mod = 30`, `Act = 7`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.9 `refresh` (Action 8)

- **模块与动作标识**：`Mod = 30`, `Act = 8`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.10 `get_player_take_bible` (Action 9)

- **模块与动作标识**：`Mod = 30`, `Act = 9`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`12` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.11 `start_take_bible` (Action 10)

- **模块与动作标识**：`Mod = 30`, `Act = 10`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.12 `rob` (Action 11)

- **模块与动作标识**：`Mod = 30`, `Act = 11`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `Tuple(7)` | `Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.13 `notify` (Action 12)

- **模块与动作标识**：`Mod = 30`, `Act = 12`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(7)` | `Tuple[int, str, int, str, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(3)` | `Tuple[int, str, int]` | 网络大端序编解码 |
  | `field_3` | `Tuple(8)` | `Tuple[int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_4` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_5` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_6` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

### 2.14 `notify_global` (Action 13)

- **模块与动作标识**：`Mod = 30`, `Act = 13`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[str, int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(3)` | `Tuple[str, str, int]` | 网络大端序编解码 |
  | `field_3` | `Tuple(4)` | `Tuple[int, str, int, int]` | 网络大端序编解码 |

### 2.15 `quickly` (Action 14)

- **模块与动作标识**：`Mod = 30`, `Act = 14`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.16 `get_take_bible_updata_data` (Action 15)

- **模块与动作标识**：`Mod = 30`, `Act = 15`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.17 `get_rob_take_bible_cd_time` (Action 16)

- **模块与动作标识**：`Mod = 30`, `Act = 16`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.18 `clear_rob_take_bible_cd_time` (Action 17)

- **模块与动作标识**：`Mod = 30`, `Act = 17`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.19 `buy_bless` (Action 18)

- **模块与动作标识**：`Mod = 30`, `Act = 18`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.22 `get_player_take_bible_monster` (Action 21)

- **模块与动作标识**：`Mod = 30`, `Act = 21`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.23 `notify_kill_monster` (Action 22)

- **模块与动作标识**：`Mod = 30`, `Act = 22`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.24 `get_recent_rob_player` (Action 23)

- **模块与动作标识**：`Mod = 30`, `Act = 23`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_30_takebible import (
    TakebibleOpenTakeBibleReq,
    TakebibleOpenTakeBibleResp,
)

# 发起 Mod 30 业务请求
```

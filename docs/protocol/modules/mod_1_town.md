# Town 模块协议规约 (Mod 1)

> **模块编号**：`1`  
> **官方类名**：`com.protocols::Mod_Town_Base`  
> **动作总数**：`14` 个  
> **常量总数**：`15` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `BECOME_IMMORTAL` | `10` | 业务状态或错误枚举码 |
| `FAILED` | `1` | 业务状态或错误枚举码 |
| `FALSE` | `12` | 业务状态或错误枚举码 |
| `FINISHED_PRACTICE` | `6` | 业务状态或错误枚举码 |
| `FULL` | `2` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `3` | 业务状态或错误枚举码 |
| `NOT_IMMORTAL` | `9` | 业务状态或错误枚举码 |
| `OFF_PRACTICE` | `5` | 业务状态或错误枚举码 |
| `ON_PRACTICE` | `4` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |
| `TOWN_FAILURE` | `14` | 业务状态或错误枚举码 |
| `TOWN_HIDDEN` | `7` | 业务状态或错误枚举码 |
| `TOWN_NOHIDDEN` | `8` | 业务状态或错误枚举码 |
| `TOWN_SUCCESS` | `13` | 业务状态或错误枚举码 |
| `TRUE` | `11` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `enter_town` (Action 0)

- **模块与动作标识**：`Mod = 1`, `Act = 0`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`41` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `Tuple(4)` | `Tuple[int, int, int, int]` | 网络大端序编解码 |
  | `field_5` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_6` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_17` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_18` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_19` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_20` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_21` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_22` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_23` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_24` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_25` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_26` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_27` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_28` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_29` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_30` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_31` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_32` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_33` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_34` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_35` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_36` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_37` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_38` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_39` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_40` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.2 `leave_town` (Action 1)

- **模块与动作标识**：`Mod = 1`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.3 `move_to` (Action 2)

- **模块与动作标识**：`Mod = 1`, `Act = 2`
- **请求参数字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.4 `get_players` (Action 3)

- **模块与动作标识**：`Mod = 1`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(36)` | `Tuple[int, int, int, Tuple[int, int, int, int], str, int, int, int, int, int, int, int, int, int, int, str, int, int, int, int, int, int, int, int, int, int, str, int, int, str, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.5 `player_follow_role_change` (Action 4)

- **模块与动作标识**：`Mod = 1`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`10` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.6 `player_count` (Action 5)

- **模块与动作标识**：`Mod = 1`, `Act = 5`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.7 `player_follow_setting_change` (Action 6)

- **模块与动作标识**：`Mod = 1`, `Act = 6`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.8 `play_town_video` (Action 7)

- **模块与动作标识**：`Mod = 1`, `Act = 7`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.9 `notify_player_have_follow_setting` (Action 8)

- **模块与动作标识**：`Mod = 1`, `Act = 8`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.10 `notify_image_change` (Action 9)

- **模块与动作标识**：`Mod = 1`, `Act = 9`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.11 `notify_dance_action` (Action 10)

- **模块与动作标识**：`Mod = 1`, `Act = 10`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.12 `player_chaos_monster_follow_change` (Action 11)

- **模块与动作标识**：`Mod = 1`, `Act = 11`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.13 `player_dragon_ball_follow_setting_change` (Action 12)

- **模块与动作标识**：`Mod = 1`, `Act = 12`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.14 `player_supreme_vip_prefix_change` (Action 13)

- **模块与动作标识**：`Mod = 1`, `Act = 13`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_1_town import (
    TownEnterTownReq,
    TownEnterTownResp,
)

# 发起 Mod 1 业务请求
# req = TownEnterTownReq(...)
# payload = req.encode_payload()
```

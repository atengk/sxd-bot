# WorldBoss 模块协议规约 (Mod 24)

> **模块编号**：`24`  
> **官方类名**：`com.protocols::Mod_WorldBoss_Base`  
> **动作总数**：`20` 个  
> **常量总数**：`10` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `ACTION_FAILED` | `1` | 业务状态或错误枚举码 |
| `ACTION_SUCCESS` | `0` | 业务状态或错误枚举码 |
| `COMBAT_LIMIT` | `9` | 业务状态或错误枚举码 |
| `DEATH_STATUS` | `5` | 业务状态或错误枚举码 |
| `MAX_TIMES` | `7` | 业务状态或错误枚举码 |
| `MISSION_OVER` | `3` | 业务状态或错误枚举码 |
| `NOT_BEGIN` | `2` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `6` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_SKILL` | `8` | 业务状态或错误枚举码 |
| `WORLD_BOSS_DEAD` | `4` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `get_world_boss_list` (Action 0)

- **模块与动作标识**：`Mod = 24`, `Act = 0`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(11)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.2 `get_world_boss_data` (Action 1)

- **模块与动作标识**：`Mod = 24`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`12` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.3 `fight_world_boss` (Action 2)

- **模块与动作标识**：`Mod = 24`, `Act = 2`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(7)` | `Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]` | 网络大端序编解码 |
  | `field_3` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.4 `clear_death_cd` (Action 3)

- **模块与动作标识**：`Mod = 24`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.5 `get_defeat_record_list` (Action 4)

- **模块与动作标识**：`Mod = 24`, `Act = 4`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, str, int]` | 网络大端序编解码 |

### 2.6 `reset_death_cd` (Action 5)

- **模块与动作标识**：`Mod = 24`, `Act = 5`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.7 `super_reborn` (Action 6)

- **模块与动作标识**：`Mod = 24`, `Act = 6`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.8 `strengthen_combat` (Action 7)

- **模块与动作标识**：`Mod = 24`, `Act = 7`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.9 `select_faction_boss_time` (Action 8)

- **模块与动作标识**：`Mod = 24`, `Act = 8`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.10 `open_world_boss` (Action 9)

- **模块与动作标识**：`Mod = 24`, `Act = 9`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.11 `close_world_boss` (Action 10)

- **模块与动作标识**：`Mod = 24`, `Act = 10`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(3)` | `Tuple[int, str, int]` | 网络大端序编解码 |

### 2.12 `defeat_world_boss` (Action 11)

- **模块与动作标识**：`Mod = 24`, `Act = 11`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_5` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `Tuple(3)` | `Tuple[int, str, int]` | 网络大端序编解码 |

### 2.13 `hurt_world_boss` (Action 12)

- **模块与动作标识**：`Mod = 24`, `Act = 12`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.14 `player_death_cd` (Action 13)

- **模块与动作标识**：`Mod = 24`, `Act = 13`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.15 `update_world_boss_position` (Action 14)

- **模块与动作标识**：`Mod = 24`, `Act = 14`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.16 `player_world_boss_buff` (Action 15)

- **模块与动作标识**：`Mod = 24`, `Act = 15`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.17 `faction_boss_time_list` (Action 16)

- **模块与动作标识**：`Mod = 24`, `Act = 16`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(4)` | `Tuple[int, int, int, int]` | 网络大端序编解码 |

### 2.18 `set_robot` (Action 17)

- **模块与动作标识**：`Mod = 24`, `Act = 17`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.19 `world_boss_low_health` (Action 18)

- **模块与动作标识**：`Mod = 24`, `Act = 18`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.20 `get_robot_statu` (Action 19)

- **模块与动作标识**：`Mod = 24`, `Act = 19`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_24_worldboss import (
    WorldbossGetWorldBossListReq,
    WorldbossGetWorldBossListResp,
)

# 发起 Mod 24 业务请求
# req = WorldbossGetWorldBossListReq(...)
# payload = req.encode_payload()
```

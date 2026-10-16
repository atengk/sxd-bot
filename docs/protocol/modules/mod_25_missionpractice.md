# MissionPractice 模块协议规约 (Mod 25)

> **模块编号**：`25`  
> **官方类名**：`com.protocols::Mod_MissionPractice_Base`  
> **动作总数**：`9` 个  
> **常量总数**：`8` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `BAG_FULL` | `2` | 业务状态或错误枚举码 |
| `IN_PRACTICE` | `3` | 业务状态或错误枚举码 |
| `NEW_WAR_REPORT` | `5` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `4` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_POWER` | `1` | 业务状态或错误枚举码 |
| `RANK_REPORT` | `6` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |
| `UPDATE_TIME` | `7` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `get_practice_info` (Action 0)

- **模块与动作标识**：`Mod = 25`, `Act = 0`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `LongUtil` | `int` | 网络大端序编解码 |

### 2.2 `start_practice` (Action 1)

- **模块与动作标识**：`Mod = 25`, `Act = 1`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.3 `cancel_practice` (Action 2)

- **模块与动作标识**：`Mod = 25`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.4 `quickly` (Action 3)

- **模块与动作标识**：`Mod = 25`, `Act = 3`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.5 `notify` (Action 4)

- **模块与动作标识**：`Mod = 25`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(6)` | `Tuple[int, int, int, Tuple[int, int], Tuple[int, int], int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(11)` | `Tuple[int, int, int, Tuple[int, int], Tuple[int, int], int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.6 `get_continue_practice_info` (Action 5)

- **模块与动作标识**：`Mod = 25`, `Act = 5`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.7 `continue_practice` (Action 6)

- **模块与动作标识**：`Mod = 25`, `Act = 6`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.8 `set_auto_sale_item` (Action 7)

- **模块与动作标识**：`Mod = 25`, `Act = 7`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.9 `cancel_auto_sale_item` (Action 8)

- **模块与动作标识**：`Mod = 25`, `Act = 8`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_25_missionpractice import (
    MissionpracticeGetPracticeInfoReq,
    MissionpracticeGetPracticeInfoResp,
)

# 发起 Mod 25 业务请求
# req = MissionpracticeGetPracticeInfoReq(...)
# payload = req.encode_payload()
```

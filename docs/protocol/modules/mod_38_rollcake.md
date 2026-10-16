# RollCake 模块协议规约 (Mod 38)

> **模块编号**：`38`  
> **官方类名**：`com.protocols::Mod_RollCake_Base`  
> **动作总数**：`7` 个  
> **常量总数**：`6` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `FAILURE` | `1` | 业务状态或错误枚举码 |
| `HAVE_RECORD` | `5` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `2` | 业务状态或错误枚举码 |
| `NO_CHANG_LUCK_TIMES` | `3` | 业务状态或错误枚举码 |
| `NO_RECORD` | `4` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `roll` (Action 0)

- **模块与动作标识**：`Mod = 38`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`10` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.3 `get_count` (Action 2)

- **模块与动作标识**：`Mod = 38`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.4 `reroll` (Action 3)

- **模块与动作标识**：`Mod = 38`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`11` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.5 `get_award` (Action 4)

- **模块与动作标识**：`Mod = 38`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.6 `get_state` (Action 5)

- **模块与动作标识**：`Mod = 38`, `Act = 5`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.7 `is_auto` (Action 6)

- **模块与动作标识**：`Mod = 38`, `Act = 6`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.8 `set_auto` (Action 7)

- **模块与动作标识**：`Mod = 38`, `Act = 7`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_38_rollcake import (
    RollcakeRollReq,
    RollcakeRollResp,
)

# 发起 Mod 38 业务请求
```

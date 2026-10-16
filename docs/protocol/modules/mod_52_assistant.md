# Assistant 模块协议规约 (Mod 52)

> **模块编号**：`52`  
> **官方类名**：`com.protocols::Mod_Assistant_Base`  
> **动作总数**：`4` 个  
> **常量总数**：`8` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `FAILED` | `5` | 业务状态或错误枚举码 |
| `FIND_IMMORTAL_LIMIT` | `7` | 业务状态或错误枚举码 |
| `FISHHOOK_LIMIT` | `6` | 业务状态或错误枚举码 |
| `HAVE_DONE` | `4` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_NUM` | `2` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_VIP` | `1` | 业务状态或错误枚举码 |
| `PACK_FULL` | `3` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `info` (Action 0)

- **模块与动作标识**：`Mod = 52`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(3)` | `Tuple[int, int, List[int]]` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.2 `get_award` (Action 1)

- **模块与动作标识**：`Mod = 52`, `Act = 1`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.3 `complete_number` (Action 2)

- **模块与动作标识**：`Mod = 52`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.4 `one_key_get_award` (Action 3)

- **模块与动作标识**：`Mod = 52`, `Act = 3`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_52_assistant import (
    AssistantInfoReq,
    AssistantInfoResp,
)

# 发起 Mod 52 业务请求
```

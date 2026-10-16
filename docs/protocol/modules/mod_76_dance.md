# Dance 模块协议规约 (Mod 76)

> **模块编号**：`76`  
> **官方类名**：`com.protocols::Mod_Dance_Base`  
> **动作总数**：`6` 个  
> **常量总数**：`2` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `ERROR` | `1` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `get_dance_info` (Action 0)

- **模块与动作标识**：`Mod = 76`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.2 `start_dance` (Action 1)

- **模块与动作标识**：`Mod = 76`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.3 `receive_award` (Action 2)

- **模块与动作标识**：`Mod = 76`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.4 `notify_start_dance` (Action 3)

- **模块与动作标识**：`Mod = 76`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.5 `notify_dance_status` (Action 4)

- **模块与动作标识**：`Mod = 76`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.6 `get_activity_open_timestamp` (Action 5)

- **模块与动作标识**：`Mod = 76`, `Act = 5`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_76_dance import (
    DanceGetDanceInfoReq,
    DanceGetDanceInfoResp,
)

# 发起 Mod 76 业务请求
```

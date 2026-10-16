# TravelEvent 模块协议规约 (Mod 21)

> **模块编号**：`21`  
> **官方类名**：`com.protocols::Mod_TravelEvent_Base`  
> **动作总数**：`5` 个  
> **常量总数**：`11` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `CD_TIME` | `0` | 业务状态或错误枚举码 |
| `COIN` | `3` | 业务状态或错误枚举码 |
| `EXP` | `4` | 业务状态或错误枚举码 |
| `FAME` | `5` | 业务状态或错误枚举码 |
| `NO_GET` | `10` | 业务状态或错误枚举码 |
| `NO_INGOT` | `8` | 业务状态或错误枚举码 |
| `PACKAGE_FULL` | `9` | 业务状态或错误枚举码 |
| `POWER` | `6` | 业务状态或错误枚举码 |
| `REACH_MAX_COUNT` | `1` | 业务状态或错误枚举码 |
| `SKILL` | `7` | 业务状态或错误枚举码 |
| `SUCCESS` | `2` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `get_activity_info` (Action 0)

- **模块与动作标识**：`Mod = 21`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.2 `get_event_and_answer` (Action 1)

- **模块与动作标识**：`Mod = 21`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `Tuple(3)` | `Tuple[int, str, str]` | 网络大端序编解码 |
  | `field_3` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.3 `answer_travel_event` (Action 2)

- **模块与动作标识**：`Mod = 21`, `Act = 2`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.4 `cancel_cd` (Action 3)

- **模块与动作标识**：`Mod = 21`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.5 `lottery_draw` (Action 4)

- **模块与动作标识**：`Mod = 21`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_21_travelevent import (
    TraveleventGetActivityInfoReq,
    TraveleventGetActivityInfoResp,
)

# 发起 Mod 21 业务请求
```

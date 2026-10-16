# WorshipMars 模块协议规约 (Mod 41)

> **模块编号**：`41`  
> **官方类名**：`com.protocols::Mod_WorshipMars_Base`  
> **动作总数**：`6` 个  
> **常量总数**：`8` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `BLESSING_TIMES` | `6` | 业务状态或错误枚举码 |
| `COUNT_USED` | `2` | 业务状态或错误枚举码 |
| `EXP_ADD` | `7` | 业务状态或错误枚举码 |
| `INSUFFICIENT_INGOT` | `3` | 业务状态或错误枚举码 |
| `INSUFFICIENT_SKILL` | `5` | 业务状态或错误枚举码 |
| `NO_ENOUGTH_VIP` | `4` | 业务状态或错误枚举码 |
| `OFFERINGS_NO_EXIST` | `1` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `mars_info` (Action 0)

- **模块与动作标识**：`Mod = 41`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `Tuple(5)` | `Tuple[int, str, int, int, int]` | 网络大端序编解码 |

### 2.2 `incense` (Action 1)

- **模块与动作标识**：`Mod = 41`, `Act = 1`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.3 `get_blessing_times_and_exp_add` (Action 2)

- **模块与动作标识**：`Mod = 41`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.4 `blessing_times_and_exp_add_notify` (Action 3)

- **模块与动作标识**：`Mod = 41`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.5 `get_remain_incense_times` (Action 4)

- **模块与动作标识**：`Mod = 41`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.6 `qingming_active_time_list` (Action 5)

- **模块与动作标识**：`Mod = 41`, `Act = 5`
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
from protocol.contracts.mod_41_worshipmars import (
    WorshipmarsMarsInfoReq,
    WorshipmarsMarsInfoResp,
)

# 发起 Mod 41 业务请求
```

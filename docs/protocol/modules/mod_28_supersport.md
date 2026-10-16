# SuperSport 模块协议规约 (Mod 28)

> **模块编号**：`28`  
> **官方类名**：`com.protocols::Mod_SuperSport_Base`  
> **动作总数**：`14` 个  
> **常量总数**：`14` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `AWARD_TOP` | `13` | 业务状态或错误枚举码 |
| `END_AWARD` | `8` | 业务状态或错误枚举码 |
| `FULL_BUY_TIMES` | `6` | 业务状态或错误枚举码 |
| `HAVE_CD_TIME` | `3` | 业务状态或错误枚举码 |
| `INVALID_RANKING` | `1` | 业务状态或错误枚举码 |
| `KILL_WIN_TOP` | `10` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_CHALLENGE_TIMES` | `2` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `5` | 业务状态或错误枚举码 |
| `NOT_IN_CHALLENGE_TIME` | `4` | 业务状态或错误枚举码 |
| `RANKING_TOP` | `11` | 业务状态或错误枚举码 |
| `START_AWARD` | `7` | 业务状态或错误枚举码 |
| `SUCCESS` | `0` | 业务状态或错误枚举码 |
| `UPDATE_RANKING_TOP` | `12` | 业务状态或错误枚举码 |
| `WIN_TOP` | `9` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `open_super_sport` (Action 0)

- **模块与动作标识**：`Mod = 28`, `Act = 0`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`14` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `Tuple(7)` | `Tuple[int, int, int, int, str, int, int]` | 网络大端序编解码 |
  | `field_13` | `Tuple(11)` | `Tuple[int, int, int, str, int, str, int, int, int, str, int]` | 网络大端序编解码 |

### 2.2 `get_challenge_list` (Action 1)

- **模块与动作标识**：`Mod = 28`, `Act = 1`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(7)` | `Tuple[int, int, int, int, str, int, int]` | 网络大端序编解码 |

### 2.3 `start_challenge` (Action 2)

- **模块与动作标识**：`Mod = 28`, `Act = 2`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(7)` | `Tuple[int, int, int, int, int, Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int], Tuple[int, int]]` | 网络大端序编解码 |

### 2.4 `clear_cd_time` (Action 3)

- **模块与动作标识**：`Mod = 28`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.5 `buy_challenge_times` (Action 4)

- **模块与动作标识**：`Mod = 28`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.6 `notify_new_sport_war_report` (Action 5)

- **模块与动作标识**：`Mod = 28`, `Act = 5`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`17` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_12` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_16` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.7 `notify` (Action 6)

- **模块与动作标识**：`Mod = 28`, `Act = 6`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.8 `close_super_sport` (Action 7)

- **模块与动作标识**：`Mod = 28`, `Act = 7`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.9 `get_player_war_report` (Action 8)

- **模块与动作标识**：`Mod = 28`, `Act = 8`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `Tuple(7)` | `Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]` | 网络大端序编解码 |
  | `field_6` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.10 `get_ranking_top` (Action 9)

- **模块与动作标识**：`Mod = 28`, `Act = 9`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(8)` | `Tuple[int, int, int, str, int, int, int, int]` | 网络大端序编解码 |

### 2.11 `notify_update_win_top` (Action 10)

- **模块与动作标识**：`Mod = 28`, `Act = 10`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.12 `notify_global` (Action 11)

- **模块与动作标识**：`Mod = 28`, `Act = 11`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, str, int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(5)` | `Tuple[int, str, int, str, int]` | 网络大端序编解码 |
  | `field_3` | `Tuple(4)` | `Tuple[int, str, int, str]` | 网络大端序编解码 |
  | `field_4` | `Tuple(3)` | `Tuple[int, str, int]` | 网络大端序编解码 |
  | `field_5` | `Tuple(5)` | `Tuple[int, int, str, int, int]` | 网络大端序编解码 |

### 2.13 `get_cd_time` (Action 12)

- **模块与动作标识**：`Mod = 28`, `Act = 12`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.14 `get_challenge_times` (Action 13)

- **模块与动作标识**：`Mod = 28`, `Act = 13`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_28_supersport import (
    SupersportOpenSuperSportReq,
    SupersportOpenSuperSportResp,
)

# 发起 Mod 28 业务请求
```

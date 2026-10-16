# Mission 模块协议规约 (Mod 4)

> **模块编号**：`4`  
> **官方类名**：`com.protocols::Mod_Mission_Base`  
> **动作总数**：`27` 个  
> **常量总数**：`49` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `ADDON_STUNT` | `1` | 业务状态或错误枚举码 |
| `ALREADY_GOT` | `42` | 业务状态或错误枚举码 |
| `AWARD_BOX_NO_OPEN` | `20` | 业务状态或错误枚举码 |
| `BACK_ATTACK` | `6` | 业务状态或错误枚举码 |
| `BE_ADDON_STUNT` | `3` | 业务状态或错误枚举码 |
| `BE_STUNT` | `2` | 业务状态或错误枚举码 |
| `COIN` | `26` | 业务状态或错误枚举码 |
| `FAILED` | `29` | 业务状态或错误枚举码 |
| `FAILURE` | `46` | 业务状态或错误枚举码 |
| `HASCHALLENGED` | `30` | 业务状态或错误枚举码 |
| `INGOT` | `27` | 业务状态或错误枚举码 |
| `LESS_POWER` | `18` | 业务状态或错误枚举码 |
| `MAGIC_ATTACK` | `7` | 业务状态或错误枚举码 |
| `MISSION_ID_ERROR` | `47` | 业务状态或错误枚举码 |
| `MS_ALREADY_CLICK` | `32` | 业务状态或错误枚举码 |
| `MS_ALREADY_DO` | `35` | 业务状态或错误枚举码 |
| `MS_ERROR_MISSION` | `31` | 业务状态或错误枚举码 |
| `MS_FAILURE` | `34` | 业务状态或错误枚举码 |
| `MS_MONSTER` | `37` | 业务状态或错误枚举码 |
| `MS_NOBODY` | `38` | 业务状态或错误枚举码 |
| `MS_PAPER` | `14` | 业务状态或错误枚举码 |
| `MS_PLAYER` | `36` | 业务状态或错误枚举码 |
| `MS_SCISSOR` | `12` | 业务状态或错误枚举码 |
| `MS_STONE` | `13` | 业务状态或错误枚举码 |
| `MS_SUCCESS` | `33` | 业务状态或错误枚举码 |
| `NORMAL_ATTACK` | `4` | 业务状态或错误枚举码 |
| `NO_BOX_TO_OPEN` | `39` | 业务状态或错误枚举码 |
| `NO_ENOUGH_STAR` | `41` | 业务状态或错误枚举码 |
| `NO_TRUNK_MISSION` | `40` | 业务状态或错误枚举码 |
| `NO_TRUNK_MISSION_COMPLETE` | `43` | 业务状态或错误枚举码 |
| `NO_UNLOCK` | `48` | 业务状态或错误枚举码 |
| `PACK_FULL` | `22` | 业务状态或错误枚举码 |
| `PICKUP_FAILED` | `24` | 业务状态或错误枚举码 |
| `PICKUP_SUCCESS` | `23` | 业务状态或错误枚举码 |
| `PRE_ATTACK` | `5` | 业务状态或错误枚举码 |
| `PRE_TRUNK_MISSION_NO_COMPLETE` | `21` | 业务状态或错误枚举码 |
| `REFIGHT` | `11` | 业务状态或错误枚举码 |
| `REPICKUP` | `25` | 业务状态或错误枚举码 |
| `SCORE_A` | `15` | 业务状态或错误枚举码 |
| `SCORE_B` | `16` | 业务状态或错误枚举码 |
| `SCORE_C` | `17` | 业务状态或错误枚举码 |
| `SEC_CHANGE` | `9` | 业务状态或错误枚举码 |
| `SELF_STUNT` | `0` | 业务状态或错误枚举码 |
| `SKILL` | `28` | 业务状态或错误枚举码 |
| `STUNT_ATTACK` | `8` | 业务状态或错误枚举码 |
| `SUCCESS` | `10` | 业务状态或错误枚举码 |
| `TRUNK_ALREADY_FIGHT` | `19` | 业务状态或错误枚举码 |
| `ZHIXIAN_BUFF` | `44` | 业务状态或错误枚举码 |
| `ZHUXIAN_BUFF` | `45` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `get_sections` (Action 0)

- **模块与动作标识**：`Mod = 4`, `Act = 0`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(6)` | `Tuple[int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.2 `enter_mission` (Action 1)

- **模块与动作标识**：`Mod = 4`, `Act = 1`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_7` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

### 2.3 `fight_monster` (Action 2)

- **模块与动作标识**：`Mod = 4`, `Act = 2`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`17` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(7)` | `Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]` | 网络大端序编解码 |
  | `field_4` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_5` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_6` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_7` | `Tuple(2)` | `Tuple[Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]], Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]]]` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_15` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.4 `rank_mission` (Action 3)

- **模块与动作标识**：`Mod = 4`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`9` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_8` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.5 `open_box` (Action 4)

- **模块与动作标识**：`Mod = 4`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.6 `pickup_award` (Action 5)

- **模块与动作标识**：`Mod = 4`, `Act = 5`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.7 `sign_play_mission_video` (Action 6)

- **模块与动作标识**：`Mod = 4`, `Act = 6`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.8 `get_monster_strategy_list` (Action 7)

- **模块与动作标识**：`Mod = 4`, `Act = 7`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(4)` | `Tuple[str, int, int, str]` | 网络大端序编解码 |

### 2.9 `get_player_war_report` (Action 8)

- **模块与动作标识**：`Mod = 4`, `Act = 8`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`12` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(7)` | `Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]` | 网络大端序编解码 |
  | `field_4` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_5` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_6` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_7` | `Tuple(2)` | `Tuple[Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]], Tuple[str, Tuple[int, str, int, int, int, int, int, int, int, int, int, int, int, int, int, int]]]` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.10 `random_item` (Action 9)

- **模块与动作标识**：`Mod = 4`, `Act = 9`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.11 `fetch_random_item` (Action 10)

- **模块与动作标识**：`Mod = 4`, `Act = 10`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.12 `get_special_result` (Action 11)

- **模块与动作标识**：`Mod = 4`, `Act = 11`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(7)` | `Tuple[int, int, Tuple[int, str, Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], Tuple[int, int, str, str, int, int, int, int, int, int, int, int, int, int, int, List[int], int, int, int, Tuple[int, int, int, int], int, int, int, int, List[int], List[int], int, List[int], int, List[int], List[int], int, int, List[int], int, int, int, int, int, int, int, Tuple[int, int], int, List[int], int, int, List[int], int, Tuple[int, str]], List[int], Tuple[int, int], int, int, int, int, int, str, int, int, Tuple[int, int, int, List[int]], int, Tuple[int, int], int, int, List[int], int, List[int], Tuple[int, int, int, int, Tuple[int, int, int, int, int], int], int, List[int], int, Tuple[str, int, int, int, Tuple[int, int], Tuple[int, int]], int, Tuple[int, int], List[int], int, int, Tuple[int, str], Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int], int]], Tuple[Tuple[int, str, Tuple[int, str], List[str], Tuple[int, int, int, int], List[str], List[str], List[str], List[str], List[str], str], Tuple[int, int, int, List[str], Tuple[int, int, int, int]], Tuple[int, int, int], Tuple[int, str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str]], Tuple[int, int, int, int, Tuple[int, int, int], str, List[int], List[str], List[str], List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[str], List[int], List[str], str, List[int], List[str], List[int], List[int], int, int, int, int, int, int, int, int, int, int, str, int, int, Tuple[int, int, Tuple[int, int], str, List[int], List[str], List[int], List[str], List[int], str, List[int], List[str], List[int], str, List[int], List[int], List[int], int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, Tuple[int, str]], Tuple[int, str], Tuple[int, int, int, int], Tuple[int, str], int, int, int], Tuple[int, int], Tuple[int, str, Tuple[int, str], List[str], List[str], List[str], List[str], List[str], List[str]], Tuple[int, int, int, int, int, int, int, int], Tuple[int, int, int, int]], int, int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.13 `is_special_scene` (Action 12)

- **模块与动作标识**：`Mod = 4`, `Act = 12`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.14 `click_mission_item_element` (Action 13)

- **模块与动作标识**：`Mod = 4`, `Act = 13`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.15 `first_tie_second_win` (Action 14)

- **模块与动作标识**：`Mod = 4`, `Act = 14`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.16 `open_box_directly` (Action 15)

- **模块与动作标识**：`Mod = 4`, `Act = 15`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.17 `pickup_trunk_mission_award_directly` (Action 16)

- **模块与动作标识**：`Mod = 4`, `Act = 16`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.18 `get_star_award` (Action 17)

- **模块与动作标识**：`Mod = 4`, `Act = 17`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.19 `get_star_award_info` (Action 18)

- **模块与动作标识**：`Mod = 4`, `Act = 18`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[ByteUtil]` | `List[int]` | 网络大端序编解码 |

### 2.20 `get_star_count` (Action 19)

- **模块与动作标识**：`Mod = 4`, `Act = 19`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.21 `get_complete_max_info` (Action 20)

- **模块与动作标识**：`Mod = 4`, `Act = 20`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.22 `get_mission_complete_info` (Action 21)

- **模块与动作标识**：`Mod = 4`, `Act = 21`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.23 `show_buff` (Action 22)

- **模块与动作标识**：`Mod = 4`, `Act = 22`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(4)` | `Tuple[int, int, int, int]` | 网络大端序编解码 |

### 2.24 `update_buff` (Action 23)

- **模块与动作标识**：`Mod = 4`, `Act = 23`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(4)` | `Tuple[int, int, int, int]` | 网络大端序编解码 |

### 2.25 `get_hire_partner_info` (Action 24)

- **模块与动作标识**：`Mod = 4`, `Act = 24`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.26 `get_sect_buff_active_flag` (Action 25)

- **模块与动作标识**：`Mod = 4`, `Act = 25`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.27 `auto_hero_fight_monster` (Action 26)

- **模块与动作标识**：`Mod = 4`, `Act = 26`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_4_mission import (
    MissionGetSectionsReq,
    MissionGetSectionsResp,
)

# 发起 Mod 4 业务请求
# req = MissionGetSectionsReq(...)
# payload = req.encode_payload()
```

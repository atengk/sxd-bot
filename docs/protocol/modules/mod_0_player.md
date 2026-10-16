# Player 模块协议规约 (Mod 0)

> **模块编号**：`0`  
> **官方类名**：`com.protocols::Mod_Player_Base`  
> **动作总数**：`69` 个  
> **常量总数**：`124` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `ACTION_FAILED` | `100` | 业务状态或错误枚举码 |
| `ACTION_SUCCESS` | `97` | 业务状态或错误枚举码 |
| `AGAINST_WALLOWS` | `3` | 业务状态或错误枚举码 |
| `ALREADY_GET` | `98` | 业务状态或错误枚举码 |
| `BAG_FULL` | `110` | 业务状态或错误枚举码 |
| `BLOODLINE_ESSENCE` | `55` | 业务状态或错误枚举码 |
| `BLUE_YUPAI` | `52` | 业务状态或错误枚举码 |
| `BUY_NUMBER` | `47` | 业务状态或错误枚举码 |
| `CAMP_ERR` | `90` | 业务状态或错误枚举码 |
| `CAMP_SALARY` | `76` | 业务状态或错误枚举码 |
| `CANCEL_PRACTICE` | `105` | 业务状态或错误枚举码 |
| `CANT_CHANGE_CAMP` | `91` | 业务状态或错误枚举码 |
| `CAN_INCENSE_COUNT` | `41` | 业务状态或错误枚举码 |
| `CAN_JUAN_DUST` | `59` | 业务状态或错误枚举码 |
| `CAN_NOT_BACK_TIMES` | `107` | 业务状态或错误枚举码 |
| `CAN_NOT_UP_HEALTH_JOIN_CAMP_WAR` | `83` | 业务状态或错误枚举码 |
| `CHARGE_BACK_EFFECT` | `117` | 业务状态或错误枚举码 |
| `DAOYUAN` | `58` | 业务状态或错误枚举码 |
| `DISABLE_LOGIN` | `6` | 业务状态或错误枚举码 |
| `DUPLICATED_NICKNAME` | `16` | 业务状态或错误枚举码 |
| `ERROR` | `111` | 业务状态或错误枚举码 |
| `EXPLOIT` | `60` | 业务状态或错误枚举码 |
| `EXTRA_POWER` | `77` | 业务状态或错误枚举码 |
| `FAILD` | `121` | 业务状态或错误枚举码 |
| `FAILED` | `1` | 业务状态或错误枚举码 |
| `FALSE` | `120` | 业务状态或错误枚举码 |
| `FAME` | `37` | 业务状态或错误枚举码 |
| `FAME_LEVEL` | `38` | 业务状态或错误枚举码 |
| `FINISHED_PRACTICE` | `104` | 业务状态或错误枚举码 |
| `FINISH_DAY_QUEST` | `85` | 业务状态或错误枚举码 |
| `FIRST_TIME` | `2` | 业务状态或错误枚举码 |
| `FISHHOOK` | `63` | 业务状态或错误枚举码 |
| `FORBIDDEN_NICKNAME` | `15` | 业务状态或错误枚举码 |
| `FREE_MEDICAL` | `75` | 业务状态或错误枚举码 |
| `FULL_BUY_TIMES` | `88` | 业务状态或错误枚举码 |
| `FUNCTION_LOCK` | `123` | 业务状态或错误枚举码 |
| `GET_ONLINE_GIFT` | `82` | 业务状态或错误枚举码 |
| `GM_LOGIN` | `8` | 业务状态或错误枚举码 |
| `GREEN_YUPAI` | `51` | 业务状态或错误枚举码 |
| `HEAD_PORTRAIT` | `65` | 业务状态或错误枚举码 |
| `HEAD_RIM` | `68` | 业务状态或错误枚举码 |
| `HEALTH_UP_MEDICAL` | `73` | 业务状态或错误枚举码 |
| `HEALTH_UP_MEDICAL_EMPTY` | `74` | 业务状态或错误枚举码 |
| `HEALTH_UP_SYS` | `72` | 业务状态或错误枚举码 |
| `HIDE_ALL_EFFECT` | `12` | 业务状态或错误枚举码 |
| `HIDE_SUSTAINTED_EFFECT` | `13` | 业务状态或错误枚举码 |
| `IDCARDISUSE` | `92` | 业务状态或错误枚举码 |
| `INTERNET_BAR_POWER` | `79` | 业务状态或错误枚举码 |
| `IP_LOGIN_LIMIT` | `7` | 业务状态或错误枚举码 |
| `KID_FES_PLAY_TIME_NOT_ENOUGTH` | `122` | 业务状态或错误枚举码 |
| `KID_LOGIN_CONTROL` | `4` | 业务状态或错误枚举码 |
| `KID_PLAY_TIME_NOT_ENOUGTH` | `5` | 业务状态或错误枚举码 |
| `MAGIC_BREATH` | `61` | 业务状态或错误枚举码 |
| `MAX_EXTRA_POWER` | `78` | 业务状态或错误枚举码 |
| `MAX_HERO_MISSION_LOCK` | `48` | 业务状态或错误枚举码 |
| `MAX_INTERNET_BAR_POWER` | `80` | 业务状态或错误枚举码 |
| `MAX_MISSION_LOCK` | `44` | 业务状态或错误枚举码 |
| `MOUNT_RUNE` | `64` | 业务状态或错误枚举码 |
| `MUSIC_SET` | `112` | 业务状态或错误枚举码 |
| `NO` | `10` | 业务状态或错误枚举码 |
| `NOT_BUY_TRAIL` | `118` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_INGOT` | `87` | 业务状态或错误枚举码 |
| `NOT_JOIN_CAMP` | `99` | 业务状态或错误枚举码 |
| `NO_INGOT` | `106` | 业务状态或错误枚举码 |
| `ONE_WARNING` | `93` | 业务状态或错误枚举码 |
| `ONLINE_GIFT` | `81` | 业务状态或错误枚举码 |
| `PACK_FULL` | `101` | 业务状态或错误枚举码 |
| `PLAYER_AVATAR` | `31` | 业务状态或错误枚举码 |
| `PLAYER_AVATAR_CD` | `32` | 业务状态或错误枚举码 |
| `PLAYER_CAMP_ID` | `36` | 业务状态或错误枚举码 |
| `PLAYER_CD_TIME` | `40` | 业务状态或错误枚举码 |
| `PLAYER_COINS` | `20` | 业务状态或错误枚举码 |
| `PLAYER_DAY_QUEST` | `84` | 业务状态或错误枚举码 |
| `PLAYER_EXPERIENCE` | `25` | 业务状态或错误枚举码 |
| `PLAYER_FUNCTION` | `34` | 业务状态或错误枚举码 |
| `PLAYER_HEALTH` | `21` | 业务状态或错误枚举码 |
| `PLAYER_INGOT` | `19` | 业务状态或错误枚举码 |
| `PLAYER_INIT_MEDICAL` | `28` | 业务状态或错误枚举码 |
| `PLAYER_LEVEL` | `18` | 业务状态或错误枚举码 |
| `PLAYER_MAX_EXPERIENCE` | `26` | 业务状态或错误枚举码 |
| `PLAYER_MAX_HEALTH` | `22` | 业务状态或错误枚举码 |
| `PLAYER_MAX_POWER` | `24` | 业务状态或错误枚举码 |
| `PLAYER_MEDICAL` | `27` | 业务状态或错误枚举码 |
| `PLAYER_PACK_EMPTY_NUM` | `33` | 业务状态或错误枚举码 |
| `PLAYER_POWER` | `23` | 业务状态或错误枚举码 |
| `PLAYER_QUEST_STATE` | `35` | 业务状态或错误枚举码 |
| `PLAYER_RECHARGE_VOUCHER` | `69` | 业务状态或错误枚举码 |
| `PLAYER_ROLE_LEVEL` | `70` | 业务状态或错误枚举码 |
| `PLAYER_SKILL` | `42` | 业务状态或错误枚举码 |
| `PLAYER_TOWN_KEY` | `71` | 业务状态或错误枚举码 |
| `PLAYER_TRANSPORT` | `29` | 业务状态或错误枚举码 |
| `PLAYER_TRANSPORT_BUFF_TIME` | `30` | 业务状态或错误枚举码 |
| `PLAYER_XIAN_LING` | `49` | 业务状态或错误枚举码 |
| `POWER_CRYSTAL` | `66` | 业务状态或错误枚举码 |
| `PURPLE_YUPAI` | `53` | 业务状态或错误枚举码 |
| `QUEST_GIFT_BAG` | `43` | 业务状态或错误枚举码 |
| `ROLE_SCRAP` | `56` | 业务状态或错误枚举码 |
| `SET_FAILED` | `109` | 业务状态或错误枚举码 |
| `SET_SUCCESS` | `108` | 业务状态或错误枚举码 |
| `SHOW_ALL_EFFECT` | `11` | 业务状态或错误枚举码 |
| `SHOW_MOUNT_TRAIL` | `116` | 业务状态或错误枚举码 |
| `SHOW_SUIT_TRAIL` | `115` | 业务状态或错误枚举码 |
| `SIMPLE_EFFECT` | `14` | 业务状态或错误枚举码 |
| `SPEAKER` | `62` | 业务状态或错误枚举码 |
| `START_PRACTICE` | `103` | 业务状态或错误枚举码 |
| `STATE_POINT` | `45` | 业务状态或错误枚举码 |
| `SUCCEED` | `0` | 业务状态或错误枚举码 |
| `SUCCESS` | `89` | 业务状态或错误枚举码 |
| `SUPER_TOWN_LEVLE` | `57` | 业务状态或错误枚举码 |
| `TANG_YUAN` | `86` | 业务状态或错误枚举码 |
| `TIMEUP` | `96` | 业务状态或错误枚举码 |
| `TOOLONG_NICKNAME` | `17` | 业务状态或错误枚举码 |
| `TOTAL_STATE_POINT` | `46` | 业务状态或错误枚举码 |
| `TRUE` | `119` | 业务状态或错误枚举码 |
| `TWO_WARNING` | `94` | 业务状态或错误枚举码 |
| `UI_TYPE` | `114` | 业务状态或错误枚举码 |
| `UPDATE_PRACTICE` | `102` | 业务状态或错误枚举码 |
| `VIP_LEVEL` | `39` | 业务状态或错误枚举码 |
| `WARNING` | `95` | 业务状态或错误枚举码 |
| `WAR_SET` | `113` | 业务状态或错误枚举码 |
| `WHITE_YU_PAI` | `50` | 业务状态或错误枚举码 |
| `XIU_WEI_LING_SHU_LEVEL` | `67` | 业务状态或错误枚举码 |
| `YELLOW_YUPAI` | `54` | 业务状态或错误枚举码 |
| `YES` | `9` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.1 `login` (Action 0)

- **模块与动作标识**：`Mod = 0`, `Act = 0`
- **请求参数字段** (`12` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_3` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_9` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_10` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `StringUtil` | `str` | 网络大端序编解码 |

- **响应回包字段** (`10` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.2 `player_first_init` (Action 1)

- **模块与动作标识**：`Mod = 0`, `Act = 1`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.3 `get_player_info` (Action 2)

- **模块与动作标识**：`Mod = 0`, `Act = 2`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`44` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_17` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_18` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_19` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_20` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_21` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_22` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_23` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_24` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_25` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_26` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_27` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_28` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_29` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_30` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_31` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_32` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_33` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_34` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_35` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_36` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_37` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_38` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_39` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_40` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_41` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_42` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_43` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.4 `update_player_data` (Action 3)

- **模块与动作标识**：`Mod = 0`, `Act = 3`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.5 `update_player_data_for_town` (Action 4)

- **模块与动作标识**：`Mod = 0`, `Act = 4`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.6 `buy_power` (Action 5)

- **模块与动作标识**：`Mod = 0`, `Act = 5`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.7 `get_player_function` (Action 6)

- **模块与动作标识**：`Mod = 0`, `Act = 6`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.8 `sign_play_player_function` (Action 7)

- **模块与动作标识**：`Mod = 0`, `Act = 7`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.9 `set_player_camp` (Action 8)

- **模块与动作标识**：`Mod = 0`, `Act = 8`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.10 `receive_player_delay_notify_message` (Action 9)

- **模块与动作标识**：`Mod = 0`, `Act = 9`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[str, int]` | 网络大端序编解码 |

### 2.11 `validate_id_card` (Action 10)

- **模块与动作标识**：`Mod = 0`, `Act = 10`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.12 `against_wallows_notify` (Action 11)

- **模块与动作标识**：`Mod = 0`, `Act = 11`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.21 `get_player_camp_salary` (Action 20)

- **模块与动作标识**：`Mod = 0`, `Act = 20`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.23 `server_time` (Action 22)

- **模块与动作标识**：`Mod = 0`, `Act = 22`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.24 `get_buy_power_data` (Action 23)

- **模块与动作标识**：`Mod = 0`, `Act = 23`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.25 `get_other_player_info` (Action 24)

- **模块与动作标识**：`Mod = 0`, `Act = 24`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.31 `player_get_online_gift` (Action 30)

- **模块与动作标识**：`Mod = 0`, `Act = 30`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.32 `get_player_current_online_gift` (Action 31)

- **模块与动作标识**：`Mod = 0`, `Act = 31`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.36 `get_affiche_list` (Action 35)

- **模块与动作标识**：`Mod = 0`, `Act = 35`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, str]` | 网络大端序编解码 |

### 2.37 `start_practice` (Action 36)

- **模块与动作标识**：`Mod = 0`, `Act = 36`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.38 `get_practice_data` (Action 37)

- **模块与动作标识**：`Mod = 0`, `Act = 37`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`8` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.39 `sign_finished_practice` (Action 38)

- **模块与动作标识**：`Mod = 0`, `Act = 38`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.40 `cancel_practice` (Action 39)

- **模块与动作标识**：`Mod = 0`, `Act = 39`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.41 `practice_notify` (Action 40)

- **模块与动作标识**：`Mod = 0`, `Act = 40`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.42 `get_player_war_cd_time` (Action 41)

- **模块与动作标识**：`Mod = 0`, `Act = 41`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.43 `get_game_assistant_info` (Action 42)

- **模块与动作标识**：`Mod = 0`, `Act = 42`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`35` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_17` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_18` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_19` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_20` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_21` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_22` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_23` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_24` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_25` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_26` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_27` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_28` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_29` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_30` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_31` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_32` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_33` | `Tuple(4)` | `Tuple[int, int, int, int]` | 网络大端序编解码 |
  | `field_34` | `Tuple(4)` | `Tuple[int, int, int, int]` | 网络大端序编解码 |

### 2.44 `send_ingot_receive_show_vip` (Action 43)

- **模块与动作标识**：`Mod = 0`, `Act = 43`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.45 `against_wallows_info` (Action 44)

- **模块与动作标识**：`Mod = 0`, `Act = 44`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.46 `get_last_player_version` (Action 45)

- **模块与动作标识**：`Mod = 0`, `Act = 45`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.47 `get_warning_affiche` (Action 46)

- **模块与动作标识**：`Mod = 0`, `Act = 46`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.48 `back_times` (Action 47)

- **模块与动作标识**：`Mod = 0`, `Act = 47`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.49 `player_info_contrast` (Action 48)

- **模块与动作标识**：`Mod = 0`, `Act = 48`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(11)` | `Tuple[int, int, str, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.50 `player_consume_alert_set_info` (Action 49)

- **模块与动作标识**：`Mod = 0`, `Act = 49`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.51 `player_consume_alert_set` (Action 50)

- **模块与动作标识**：`Mod = 0`, `Act = 50`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.52 `get_player_info_by_username` (Action 51)

- **模块与动作标识**：`Mod = 0`, `Act = 51`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `StringUtil` | `str` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.53 `player_follow_setting` (Action 52)

- **模块与动作标识**：`Mod = 0`, `Act = 52`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.54 `is_weichengnian` (Action 53)

- **模块与动作标识**：`Mod = 0`, `Act = 53`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.55 `set_custom_pannel` (Action 54)

- **模块与动作标识**：`Mod = 0`, `Act = 54`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.56 `pc_client_gift_info` (Action 55)

- **模块与动作标识**：`Mod = 0`, `Act = 55`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.57 `receive_client_gift` (Action 56)

- **模块与动作标识**：`Mod = 0`, `Act = 56`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.58 `notify_have_client_gift` (Action 57)

- **模块与动作标识**：`Mod = 0`, `Act = 57`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.59 `gamebang_player_status` (Action 58)

- **模块与动作标识**：`Mod = 0`, `Act = 58`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.60 `set_player_setting` (Action 59)

- **模块与动作标识**：`Mod = 0`, `Act = 59`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.61 `player_open_new_game_function` (Action 60)

- **模块与动作标识**：`Mod = 0`, `Act = 60`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[ShortUtil]` | `List[int]` | 网络大端序编解码 |

### 2.62 `player_get_internet_bar_online_gift` (Action 61)

- **模块与动作标识**：`Mod = 0`, `Act = 61`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.63 `get_player_current_internet_bar_online_gift` (Action 62)

- **模块与动作标识**：`Mod = 0`, `Act = 62`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.64 `set_in_st_town` (Action 63)

- **模块与动作标识**：`Mod = 0`, `Act = 63`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.65 `is_in_st_town` (Action 64)

- **模块与动作标识**：`Mod = 0`, `Act = 64`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.66 `super_town_level_info` (Action 65)

- **模块与动作标识**：`Mod = 0`, `Act = 65`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.67 `compare_war_power` (Action 66)

- **模块与动作标识**：`Mod = 0`, `Act = 66`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(21)` | `Tuple[str, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.68 `operation_activity_time_list` (Action 67)

- **模块与动作标识**：`Mod = 0`, `Act = 67`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(4)` | `Tuple[int, Tuple[int, int], int, int]` | 网络大端序编解码 |

### 2.69 `is_test_server` (Action 68)

- **模块与动作标识**：`Mod = 0`, `Act = 68`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.70 `check_function_open` (Action 69)

- **模块与动作标识**：`Mod = 0`, `Act = 69`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.71 `player_ui_list` (Action 70)

- **模块与动作标识**：`Mod = 0`, `Act = 70`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.72 `set_player_ui` (Action 71)

- **模块与动作标识**：`Mod = 0`, `Act = 71`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.73 `get_player_mission_loading_interface_id` (Action 72)

- **模块与动作标识**：`Mod = 0`, `Act = 72`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

### 2.74 `set_player_mission_loading_interface_id` (Action 73)

- **模块与动作标识**：`Mod = 0`, `Act = 73`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.75 `award_item_notify` (Action 74)

- **模块与动作标识**：`Mod = 0`, `Act = 74`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.76 `heart` (Action 75)

- **模块与动作标识**：`Mod = 0`, `Act = 75`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.77 `customer_service_info` (Action 76)

- **模块与动作标识**：`Mod = 0`, `Act = 76`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `LongUtil` | `int` | 网络大端序编解码 |

### 2.78 `set_get_customer_service_gift` (Action 77)

- **模块与动作标识**：`Mod = 0`, `Act = 77`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.79 `kid_login_notify` (Action 78)

- **模块与动作标识**：`Mod = 0`, `Act = 78`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.80 `get_player_lock` (Action 79)

- **模块与动作标识**：`Mod = 0`, `Act = 79`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.81 `get_charge_back_effect_list` (Action 80)

- **模块与动作标识**：`Mod = 0`, `Act = 80`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.82 `player_chaos_monster_follow_setting` (Action 81)

- **模块与动作标识**：`Mod = 0`, `Act = 81`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.83 `player_dragon_ball_follow_setting` (Action 82)

- **模块与动作标识**：`Mod = 0`, `Act = 82`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.84 `get_head_info` (Action 83)

- **模块与动作标识**：`Mod = 0`, `Act = 83`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.85 `official_account_panel_show_flag` (Action 84)

- **模块与动作标识**：`Mod = 0`, `Act = 84`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.100 `jiekou_test` (Action 99)

- **模块与动作标识**：`Mod = 0`, `Act = 99`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`0` 项):
  *(无返回值)*

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_0_player import (
    PlayerLoginReq,
    PlayerLoginResp,
)

# 发起 Mod 0 业务请求
# req = PlayerLoginReq(...)
# payload = req.encode_payload()
```

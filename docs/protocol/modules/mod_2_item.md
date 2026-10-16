# Item 模块协议规约 (Mod 2)

> **模块编号**：`2`  
> **官方类名**：`com.protocols::Mod_Item_Base`  
> **动作总数**：`113` 个  
> **常量总数**：`231` 个  
> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)

---

## 1. 业务模块常量定义 (Constants)

| 常量名 | 数值 | 业务含义说明 |
| :--- | :--- | :--- |
| `ACTION_FAILED` | `143` | 业务状态或错误枚举码 |
| `ACTION_SUCCESS` | `20` | 业务状态或错误枚举码 |
| `ALREADY_HAVE` | `162` | 业务状态或错误枚举码 |
| `ALREADY_MARRY` | `213` | 业务状态或错误枚举码 |
| `AMAGIC_EQUIP` | `204` | 业务状态或错误枚举码 |
| `AMAGIC_SPIRIT` | `205` | 业务状态或错误枚举码 |
| `ARMOR_FUN_NOT_OPEN` | `72` | 业务状态或错误枚举码 |
| `ARTIFACT` | `202` | 业务状态或错误枚举码 |
| `ARTIFACT_NOT_OPEN` | `113` | 业务状态或错误枚举码 |
| `ATTRIBUTE_GOD_STONE` | `198` | 业务状态或错误枚举码 |
| `AWAKE_NO_OPEN` | `80` | 业务状态或错误枚举码 |
| `BAI_LIAN_QIAN_KUN_TWO_UNOPEN` | `99` | 业务状态或错误枚举码 |
| `BAI_LIAN_QIAN_KUN_UNOPEN` | `90` | 业务状态或错误枚举码 |
| `BECOME_IMMORTAL_FUN_NOT_OPEN` | `63` | 业务状态或错误枚举码 |
| `BLOODLINE` | `191` | 业务状态或错误枚举码 |
| `BLOODLINE_FUN_NOT_OPEN` | `64` | 业务状态或错误枚举码 |
| `BLOOD_ESSENCE` | `7` | 业务状态或错误枚举码 |
| `BOOK_ERROR` | `216` | 业务状态或错误枚举码 |
| `BUY_NUMBER_LIMIT` | `185` | 业务状态或错误枚举码 |
| `CAN_JUAN_PACK_FULL` | `76` | 业务状态或错误枚举码 |
| `CARD_SOUL_FUN_NOT_OPEN` | `73` | 业务状态或错误枚举码 |
| `CHANGE_CARD_NOT_OPEN` | `109` | 业务状态或错误枚举码 |
| `CHAOSVOID_FUN_NOT_OPEN` | `54` | 业务状态或错误枚举码 |
| `CHAOS_ITEM_PACK_FULL` | `59` | 业务状态或错误枚举码 |
| `CHAOS_LING_YE` | `15` | 业务状态或错误枚举码 |
| `CHAOS_MONSTER_PACK_FULL` | `58` | 业务状态或错误枚举码 |
| `CHAOS_NO_OPEN` | `95` | 业务状态或错误枚举码 |
| `CHAOS_VOID` | `189` | 业务状态或错误枚举码 |
| `CHILDREN_COUNT_LIMIT` | `98` | 业务状态或错误枚举码 |
| `CHILDREN_FUNCTION_UNOPEN` | `97` | 业务状态或错误枚举码 |
| `COINS` | `3` | 业务状态或错误枚举码 |
| `DANCE_ACTION_NOT_OPEN` | `106` | 业务状态或错误枚举码 |
| `DAO_YUAN` | `16` | 业务状态或错误枚举码 |
| `DAO_YUAN_CAN_NOT_GET` | `67` | 业务状态或错误枚举码 |
| `DESTINY_SWORD` | `203` | 业务状态或错误枚举码 |
| `DEVILEXPEDITION_NOT_OPEN` | `122` | 业务状态或错误枚举码 |
| `DRAGONBALL` | `13` | 业务状态或错误枚举码 |
| `DRAGONBALL_FUN_NOT_OPEN` | `55` | 业务状态或错误枚举码 |
| `DRAGONBALL_NO_FREE_GRID` | `57` | 业务状态或错误枚举码 |
| `DRAGONBALL_VOW_FUN_NOT_OPEN` | `56` | 业务状态或错误枚举码 |
| `DRAG_FAILED` | `182` | 业务状态或错误枚举码 |
| `DRAG_SUCCESS` | `180` | 业务状态或错误枚举码 |
| `DRAG_TO_BAG` | `178` | 业务状态或错误枚举码 |
| `DRAG_TO_FURNACE` | `179` | 业务状态或错误枚举码 |
| `EIGHTIMMORTALS_NOT_OPEN` | `111` | 业务状态或错误枚举码 |
| `ELIXIR_SOUL_NOT_OPEN` | `107` | 业务状态或错误枚举码 |
| `END_TIME` | `48` | 业务状态或错误枚举码 |
| `EQUIP` | `186` | 业务状态或错误枚举码 |
| `EQUIPMENT_NOT_IN_BODY` | `159` | 业务状态或错误枚举码 |
| `ERROR_COOL_TIME` | `119` | 业务状态或错误枚举码 |
| `ERROR_PARAM` | `230` | 业务状态或错误枚举码 |
| `EUDEMONS_FUN_NOT_OPENED` | `130` | 业务状态或错误枚举码 |
| `EXISTS_NICK_NAME` | `208` | 业务状态或错误枚举码 |
| `EXPLOIT` | `17` | 业务状态或错误枚举码 |
| `FAILED` | `153` | 业务状态或错误枚举码 |
| `FAILED_TOWN` | `93` | 业务状态或错误枚举码 |
| `FAILURE` | `224` | 业务状态或错误枚举码 |
| `FALLING` | `155` | 业务状态或错误枚举码 |
| `FAME` | `4` | 业务状态或错误枚举码 |
| `FATE` | `188` | 业务状态或错误枚举码 |
| `FATE_FUN_NOT_OPEN` | `53` | 业务状态或错误枚举码 |
| `FATE_INN_NOT_UPGRADE` | `100` | 业务状态或错误枚举码 |
| `FATE_PACK_FULL` | `207` | 业务状态或错误枚举码 |
| `FA_FANG` | `169` | 业务状态或错误枚举码 |
| `FA_GONG` | `166` | 业务状态或错误枚举码 |
| `FA_XIANG_NO_OPEN` | `114` | 业务状态或错误枚举码 |
| `FIND_IMMORTAL_FUN_NOT_OPEN` | `51` | 业务状态或错误枚举码 |
| `FISHING_NOT_OPEN` | `79` | 业务状态或错误枚举码 |
| `FIVE_BLESSINGS_FUN_NOT_OPEN` | `77` | 业务状态或错误枚举码 |
| `FIVE_ELEMENTS_FUN_NOT_OPEN` | `74` | 业务状态或错误枚举码 |
| `FIVE_ELEMENTS_STONE` | `192` | 业务状态或错误枚举码 |
| `FLOP_GAME_FUN_NOT_OPEN` | `71` | 业务状态或错误枚举码 |
| `FORBID` | `212` | 业务状态或错误枚举码 |
| `FORBIDDEN_NICKNAME` | `210` | 业务状态或错误枚举码 |
| `FUN_NOT_OPEN` | `25` | 业务状态或错误枚举码 |
| `GIFT_ID` | `12` | 业务状态或错误枚举码 |
| `GOLDEN_DAN` | `193` | 业务状态或错误枚举码 |
| `GRID_ID_ERROR` | `219` | 业务状态或错误枚举码 |
| `GRID_MAX_LIMIT` | `220` | 业务状态或错误枚举码 |
| `HAS_ACTIVATED_TOMB_ARTIFACTS` | `138` | 业务状态或错误枚举码 |
| `HAS_NO_CHENG_NIAN_CHILD` | `105` | 业务状态或错误枚举码 |
| `HAVE_JEWEL` | `32` | 业务状态或错误枚举码 |
| `HAVE_NO_ROLE_CAN_TO_SAGE` | `66` | 业务状态或错误枚举码 |
| `HAVE_SOUL` | `31` | 业务状态或错误枚举码 |
| `HOLDING` | `156` | 业务状态或错误枚举码 |
| `HORSE_SKILL` | `199` | 业务状态或错误枚举码 |
| `HORSE_SKILL_NOT_OPEN` | `103` | 业务状态或错误枚举码 |
| `INGOT` | `2` | 业务状态或错误枚举码 |
| `INSUFFICIENT_CARD` | `150` | 业务状态或错误枚举码 |
| `INSUFFICIENT_COIN` | `147` | 业务状态或错误枚举码 |
| `INSUFFICIENT_INGOT` | `24` | 业务状态或错误枚举码 |
| `INSUFFICIENT_YUPAI` | `183` | 业务状态或错误枚举码 |
| `IN_CAMP_WAR` | `43` | 业务状态或错误枚举码 |
| `IN_FACTION_WAR` | `44` | 业务状态或错误枚举码 |
| `IN_HEROES_WAR` | `45` | 业务状态或错误枚举码 |
| `IS_DAY_FALL` | `133` | 业务状态或错误枚举码 |
| `ITEM_ERROR` | `215` | 业务状态或错误枚举码 |
| `ITEM_ID` | `19` | 业务状态或错误枚举码 |
| `ITEM_LIST_REFRESHED` | `151` | 业务状态或错误枚举码 |
| `ITEM_LOCK` | `144` | 业务状态或错误枚举码 |
| `ITEM_NO_EXIST` | `152` | 业务状态或错误枚举码 |
| `JEWEL_FUN_NOT_OPEN` | `75` | 业务状态或错误枚举码 |
| `JOB_NOT_MATCH` | `42` | 业务状态或错误枚举码 |
| `JOB_STRENGTHEN` | `200` | 业务状态或错误枚举码 |
| `JOB_STRENGTHEN_NOT_OPEN` | `110` | 业务状态或错误枚举码 |
| `JUE_FANG` | `170` | 业务状态或错误枚举码 |
| `JUE_GONG` | `167` | 业务状态或错误枚举码 |
| `JULING_FUN_NO_OPEN` | `81` | 业务状态或错误枚举码 |
| `JUYUAN` | `194` | 业务状态或错误枚举码 |
| `JUYUAN_NO_OPEN` | `86` | 业务状态或错误枚举码 |
| `LINK_FATE_NO_OPEN` | `84` | 业务状态或错误枚举码 |
| `LINK_FATE_STONE_PACK_FULL` | `85` | 业务状态或错误枚举码 |
| `LIU_DAO_LUN_HUI_NOT_OPEN` | `121` | 业务状态或错误枚举码 |
| `LOST_DEPLOY_FUN_NOT_OPEN` | `78` | 业务状态或错误枚举码 |
| `LUN_HUN_NO_OPEN` | `87` | 业务状态或错误枚举码 |
| `MAGICARRAY_NO_OPEN` | `124` | 业务状态或错误枚举码 |
| `MAGIC_ARMS` | `190` | 业务状态或错误枚举码 |
| `MAGIC_ARMS_FUN_NOT_OPEN` | `65` | 业务状态或错误枚举码 |
| `MAGIC_WEAPON_NOT_OPEN` | `102` | 业务状态或错误枚举码 |
| `MAIN_ROLE_REBIRTH_NO_OPEN` | `123` | 业务状态或错误枚举码 |
| `MAIN_ROLE_SAINT_NO_OPEN` | `94` | 业务状态或错误枚举码 |
| `MATERIAL_NOT_ENOUGH` | `22` | 业务状态或错误枚举码 |
| `MAX_BUY_COUNT_LIMIT` | `225` | 业务状态或错误枚举码 |
| `MIRACLE_FIGHTERS` | `196` | 业务状态或错误枚举码 |
| `MIRACLE_FIGHTERS_TWO` | `201` | 业务状态或错误枚举码 |
| `MOUNT_FUN_NOT_OPEN` | `52` | 业务状态或错误枚举码 |
| `MOUNT_OR_SUIT_NO_OPEN` | `89` | 业务状态或错误枚举码 |
| `MOUNT_RUNE_FUNCTION_UNOPEN` | `88` | 业务状态或错误枚举码 |
| `MYSTIC_CAPTURE_NOT_OPEN` | `139` | 业务状态或错误枚举码 |
| `NIMBUS` | `14` | 业务状态或错误枚举码 |
| `NO` | `1` | 业务状态或错误枚举码 |
| `NOENOUGH_GRID` | `184` | 业务状态或错误枚举码 |
| `NOSUITEROLELEVEL` | `160` | 业务状态或错误枚举码 |
| `NOT_AWARD_ID` | `222` | 业务状态或错误枚举码 |
| `NOT_CHARGE_NUM` | `134` | 业务状态或错误枚举码 |
| `NOT_ELIXIR_ITEM` | `26` | 业务状态或错误枚举码 |
| `NOT_ELIXIR_VALUE` | `27` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_ACTIVITY` | `135` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_CHIP` | `128` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_COIN` | `116` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_DAY_COUNT` | `175` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_EXPERIENCE` | `115` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_FATE_GRID` | `46` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_FIVE_ELEMENTS_PACK` | `70` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_GRID` | `41` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_ITEM` | `171` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_LEVEL` | `28` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_ONVERT_RES` | `140` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_SOUL_GRID` | `47` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_STATE_POINT` | `174` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_STATE_POINT_LV` | `177` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_TODAY_RECHARGE_INGOT` | `120` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_VALUE` | `132` | 业务状态或错误枚举码 |
| `NOT_ENOUGH_VIP_LEVEL` | `158` | 业务状态或错误枚举码 |
| `NOT_ENOUGTH_EXP_ITEM` | `129` | 业务状态或错误枚举码 |
| `NOT_FRIEND` | `223` | 业务状态或错误枚举码 |
| `NOT_GAIN_GIFT` | `131` | 业务状态或错误枚举码 |
| `NOT_GRID` | `172` | 业务状态或错误枚举码 |
| `NOT_HAVE_ZHANG_MA_ZI` | `68` | 业务状态或错误枚举码 |
| `NOT_INVITE_ROLE` | `60` | 业务状态或错误枚举码 |
| `NOT_SELECTED` | `206` | 业务状态或错误枚举码 |
| `NOT_SUPERGIFT` | `214` | 业务状态或错误枚举码 |
| `NOUPGRADEQUEUE` | `163` | 业务状态或错误枚举码 |
| `NOVIPLEVEL` | `164` | 业务状态或错误枚举码 |
| `NO_ENOUGH` | `226` | 业务状态或错误枚举码 |
| `NO_ENOUGH_RESOURCE` | `218` | 业务状态或错误枚举码 |
| `NO_SUITE_EQUIP_TYPE` | `35` | 业务状态或错误枚举码 |
| `NO_SUITE_ROLE_JOB` | `37` | 业务状态或错误枚举码 |
| `NO_SUITE_ROLE_LEVEL` | `36` | 业务状态或错误枚举码 |
| `NO_THIS_DANCE` | `104` | 业务状态或错误枚举码 |
| `NO_TRANS_TIMES` | `227` | 业务状态或错误枚举码 |
| `NO_USE` | `176` | 业务状态或错误枚举码 |
| `NO_USE_AVATAR_CARD` | `21` | 业务状态或错误枚举码 |
| `NPC_ITEM_NO_EXIST` | `149` | 业务状态或错误枚举码 |
| `OPEN_NOT_ENOUGH_LEVEL` | `118` | 业务状态或错误枚举码 |
| `OPEN_NOT_ENOUGH_VIP_LEVEL` | `117` | 业务状态或错误枚举码 |
| `ORANGE_EQUIP` | `187` | 业务状态或错误枚举码 |
| `ORANGE_EQUIPMENT_FUN_NOT_OPEN` | `91` | 业务状态或错误枚举码 |
| `PACK_FULL` | `23` | 业务状态或错误枚举码 |
| `PAGE_ONE_LOCK` | `221` | 业务状态或错误枚举码 |
| `PARTNER_SOUL_ARRAY_NOT_OPEN` | `141` | 业务状态或错误枚举码 |
| `PARTNER_SOUL_NOT_OPEN` | `101` | 业务状态或错误枚举码 |
| `PLAYER_GRID_NO_EXIST` | `29` | 业务状态或错误枚举码 |
| `PLAYER_ROLE_NOT_EXIST` | `34` | 业务状态或错误枚举码 |
| `POWER` | `10` | 业务状态或错误枚举码 |
| `POWERFAME` | `18` | 业务状态或错误枚举码 |
| `POWER_FAME_NO_OPEN` | `82` | 业务状态或错误枚举码 |
| `PU_FANG` | `168` | 业务状态或错误枚举码 |
| `PU_GONG` | `165` | 业务状态或错误枚举码 |
| `RAISING` | `154` | 业务状态或错误枚举码 |
| `RECENTLY_CAN_BE_USED` | `62` | 业务状态或错误枚举码 |
| `RECYCLE_ITEM_EXPIRED` | `146` | 业务状态或错误枚举码 |
| `RECYCLE_ITEM_NO_EXIST` | `145` | 业务状态或错误枚举码 |
| `REFINE_POOL_UNOPEN` | `92` | 业务状态或错误枚举码 |
| `ROLE_NO_REJOIN` | `61` | 业务状态或错误枚举码 |
| `ROLE_POS_EQUI_EMPTY` | `39` | 业务状态或错误枚举码 |
| `ROLE_USED_ITEM` | `69` | 业务状态或错误枚举码 |
| `ROLL_CAKE_FUN_NOT_OPEN` | `50` | 业务状态或错误枚举码 |
| `SANT_WEAPON` | `197` | 业务状态或错误枚举码 |
| `SEAL_SOUL_NO_OPEN` | `96` | 业务状态或错误枚举码 |
| `SKILL` | `8` | 业务状态或错误枚举码 |
| `SKILL_BOOK_PACK_FULL` | `217` | 业务状态或错误枚举码 |
| `SOURCE_GRID_EMPTY` | `30` | 业务状态或错误枚举码 |
| `STATE_POINT` | `6` | 业务状态或错误枚举码 |
| `STONE` | `5` | 业务状态或错误枚举码 |
| `SUCCESS` | `161` | 业务状态或错误枚举码 |
| `TACTICS_NOT_OPEN` | `108` | 业务状态或错误枚举码 |
| `THE_SAME_NICK_NAME` | `209` | 业务状态或错误枚举码 |
| `TIAN_SHU_NO_OPEN` | `83` | 业务状态或错误枚举码 |
| `TIME_LIMIT` | `126` | 业务状态或错误枚举码 |
| `TODAY_HAS_USED` | `136` | 业务状态或错误枚举码 |
| `TOMB_ARTIFACTS_FUN_NO_OPEN` | `137` | 业务状态或错误枚举码 |
| `TOOLONG_NICKNAME` | `211` | 业务状态或错误枚举码 |
| `TOWER_FUN_NOT_OPEN` | `49` | 业务状态或错误枚举码 |
| `TOWN_NPC_ERROR` | `173` | 业务状态或错误枚举码 |
| `TYPE_ERROR` | `229` | 业务状态或错误枚举码 |
| `UNSUITED` | `148` | 业务状态或错误枚举码 |
| `UNUSABLE_ITEM` | `40` | 业务状态或错误枚举码 |
| `UN_AVALIABLE_GRID` | `38` | 业务状态或错误枚举码 |
| `WAIT_TO_USE` | `125` | 业务状态或错误枚举码 |
| `WAREHOUSE_FULL` | `33` | 业务状态或错误枚举码 |
| `WISH_BOX_NOT_EXIST` | `228` | 业务状态或错误枚举码 |
| `WRONG_ITEM` | `181` | 业务状态或错误枚举码 |
| `XIAN_LING` | `9` | 业务状态或错误枚举码 |
| `XU_YUAN_LI_JUAN_CANT_USE` | `127` | 业务状态或错误枚举码 |
| `YES` | `0` | 业务状态或错误枚举码 |
| `YIN_YANG_HALL_NOT_OPEN` | `112` | 业务状态或错误枚举码 |
| `YUPAI_NUMBER` | `11` | 业务状态或错误枚举码 |
| `YU_BAO` | `195` | 业务状态或错误枚举码 |
| `ZENG_FU_SHI_NOT_ENOUGHT` | `142` | 业务状态或错误枚举码 |
| `ZERO_CD_TIME` | `157` | 业务状态或错误枚举码 |

---

## 2. 动作与接口明细 (Actions)

### 2.2 `get_item_basical_infos` (Action 1)

- **模块与动作标识**：`Mod = 2`, `Act = 1`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(25)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, str]` | 网络大端序编解码 |

### 2.3 `get_empty_grid_number` (Action 2)

- **模块与动作标识**：`Mod = 2`, `Act = 2`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.4 `get_all_player_item_infos` (Action 3)

- **模块与动作标识**：`Mod = 2`, `Act = 3`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(21)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.5 `change_item_info_send_to_client` (Action 4)

- **模块与动作标识**：`Mod = 2`, `Act = 4`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`21` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_17` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_18` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_19` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_20` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.6 `open_notify` (Action 5)

- **模块与动作标识**：`Mod = 2`, `Act = 5`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`0` 项):
  *(无返回值)*

### 2.7 `get_player_gift_all_info` (Action 6)

- **模块与动作标识**：`Mod = 2`, `Act = 6`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(5)` | `Tuple[int, int, str, str, Tuple[int, int, int]]` | 网络大端序编解码 |

### 2.22 `get_facture_reel_data` (Action 21)

- **模块与动作标识**：`Mod = 2`, `Act = 21`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`12` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `Tuple(5)` | `Tuple[int, int, str, int, int]` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.23 `get_player_role_elixir_data` (Action 22)

- **模块与动作标识**：`Mod = 2`, `Act = 22`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.26 `avatar_card_off` (Action 25)

- **模块与动作标识**：`Mod = 2`, `Act = 25`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.28 `player_use_grid_reel` (Action 27)

- **模块与动作标识**：`Mod = 2`, `Act = 27`
- **请求参数字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.29 `player_use_grid_elixir` (Action 28)

- **模块与动作标识**：`Mod = 2`, `Act = 28`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.30 `player_get_super_gift` (Action 29)

- **模块与动作标识**：`Mod = 2`, `Act = 29`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.31 `get_player_role_elixir_record` (Action 30)

- **模块与动作标识**：`Mod = 2`, `Act = 30`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`7` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(10)` | `Tuple[int, int, int, int, int, int, int, int, int, Tuple[int, int, int]]` | 网络大端序编解码 |
  | `field_2` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.32 `player_use_ingot_elixir` (Action 31)

- **模块与动作标识**：`Mod = 2`, `Act = 31`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.42 `get_player_pack_item_list` (Action 41)

- **模块与动作标识**：`Mod = 2`, `Act = 41`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(21)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `Tuple(21)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.43 `get_player_warehouse_grids` (Action 42)

- **模块与动作标识**：`Mod = 2`, `Act = 42`
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
  | `field_3` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.44 `get_role_equip_list` (Action 43)

- **模块与动作标识**：`Mod = 2`, `Act = 43`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.45 `change_pack_item_grid` (Action 44)

- **模块与动作标识**：`Mod = 2`, `Act = 44`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.46 `change_warehouse_item_grid` (Action 45)

- **模块与动作标识**：`Mod = 2`, `Act = 45`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.47 `drop_pack_grid_item` (Action 46)

- **模块与动作标识**：`Mod = 2`, `Act = 46`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.48 `drop_warehouse_grid_item` (Action 47)

- **模块与动作标识**：`Mod = 2`, `Act = 47`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.49 `move_warehouse_grid_item_to_pack` (Action 48)

- **模块与动作标识**：`Mod = 2`, `Act = 48`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.50 `move_pack_grid_item_to_warehouse` (Action 49)

- **模块与动作标识**：`Mod = 2`, `Act = 49`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.51 `equip_player_role_item` (Action 50)

- **模块与动作标识**：`Mod = 2`, `Act = 50`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.52 `remove_player_role_equipment` (Action 51)

- **模块与动作标识**：`Mod = 2`, `Act = 51`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.53 `get_player_role_equip_list` (Action 52)

- **模块与动作标识**：`Mod = 2`, `Act = 52`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.54 `player_use_grid_item` (Action 53)

- **模块与动作标识**：`Mod = 2`, `Act = 53`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.55 `classify_pack` (Action 54)

- **模块与动作标识**：`Mod = 2`, `Act = 54`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.56 `classify_warehouse` (Action 55)

- **模块与动作标识**：`Mod = 2`, `Act = 55`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.57 `add_pack_grid` (Action 56)

- **模块与动作标识**：`Mod = 2`, `Act = 56`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.58 `add_warehouse_grid` (Action 57)

- **模块与动作标识**：`Mod = 2`, `Act = 57`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.59 `has_level_gift_item` (Action 58)

- **模块与动作标识**：`Mod = 2`, `Act = 58`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.60 `has_medical_item` (Action 59)

- **模块与动作标识**：`Mod = 2`, `Act = 59`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.72 `get_npc_item_list` (Action 71)

- **模块与动作标识**：`Mod = 2`, `Act = 71`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

### 2.73 `get_npc_recycle_item_list` (Action 72)

- **模块与动作标识**：`Mod = 2`, `Act = 72`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(7)` | `Tuple[int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.74 `player_sell_item` (Action 73)

- **模块与动作标识**：`Mod = 2`, `Act = 73`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(7)` | `Tuple[int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.75 `player_buy_back_item` (Action 74)

- **模块与动作标识**：`Mod = 2`, `Act = 74`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(7)` | `Tuple[int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.76 `player_buy_npc_item` (Action 75)

- **模块与动作标识**：`Mod = 2`, `Act = 75`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.77 `lucky_shop_item_list` (Action 76)

- **模块与动作标识**：`Mod = 2`, `Act = 76`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.78 `lucky_shop_record_list` (Action 77)

- **模块与动作标识**：`Mod = 2`, `Act = 77`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(4)` | `Tuple[int, str, int, int]` | 网络大端序编解码 |

### 2.79 `buy_lucky_shop_item` (Action 78)

- **模块与动作标识**：`Mod = 2`, `Act = 78`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.80 `refresh_lucky_shop` (Action 79)

- **模块与动作标识**：`Mod = 2`, `Act = 79`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.81 `player_buy_equip_item` (Action 80)

- **模块与动作标识**：`Mod = 2`, `Act = 80`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `LongUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.92 `get_equipment_list` (Action 91)

- **模块与动作标识**：`Mod = 2`, `Act = 91`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(8)` | `Tuple[int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.93 `equip_upgrade_stat` (Action 92)

- **模块与动作标识**：`Mod = 2`, `Act = 92`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |

### 2.95 `clear_upgrade_cd_time` (Action 94)

- **模块与动作标识**：`Mod = 2`, `Act = 94`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.96 `open_upgrade_opportunity` (Action 95)

- **模块与动作标识**：`Mod = 2`, `Act = 95`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.97 `equip_upgrade_stat_list` (Action 96)

- **模块与动作标识**：`Mod = 2`, `Act = 96`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.98 `player_reel_need_item` (Action 97)

- **模块与动作标识**：`Mod = 2`, `Act = 97`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(5)` | `Tuple[int, int, int, int, int]` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.99 `player_equip_use_reel` (Action 98)

- **模块与动作标识**：`Mod = 2`, `Act = 98`
- **请求参数字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.101 `get_player_item_facture_reel_data` (Action 100)

- **模块与动作标识**：`Mod = 2`, `Act = 100`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`6` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `Tuple(5)` | `Tuple[int, int, str, int, int]` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.102 `permanent_clean_item_update_cd` (Action 101)

- **模块与动作标识**：`Mod = 2`, `Act = 101`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.103 `get_permanent_clean_item_update_cd` (Action 102)

- **模块与动作标识**：`Mod = 2`, `Act = 102`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.104 `notify_super_gift_items` (Action 103)

- **模块与动作标识**：`Mod = 2`, `Act = 103`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`33` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_5` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_9` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_10` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_11` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_12` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_17` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_18` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_19` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_20` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_21` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_22` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_23` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_24` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_25` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_26` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_27` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_28` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_29` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_30` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_31` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |
  | `field_32` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.105 `change_attack_item` (Action 104)

- **模块与动作标识**：`Mod = 2`, `Act = 104`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.106 `change_attack_info` (Action 105)

- **模块与动作标识**：`Mod = 2`, `Act = 105`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.107 `get_soul` (Action 106)

- **模块与动作标识**：`Mod = 2`, `Act = 106`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.108 `get_the_item_num` (Action 107)

- **模块与动作标识**：`Mod = 2`, `Act = 107`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.109 `can_change_list` (Action 108)

- **模块与动作标识**：`Mod = 2`, `Act = 108`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(18)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.110 `get_gold_oil` (Action 109)

- **模块与动作标识**：`Mod = 2`, `Act = 109`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.111 `can_use_gold_info` (Action 110)

- **模块与动作标识**：`Mod = 2`, `Act = 110`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(18)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.112 `use_gold_oil` (Action 111)

- **模块与动作标识**：`Mod = 2`, `Act = 111`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.113 `take_off_clothes` (Action 112)

- **模块与动作标识**：`Mod = 2`, `Act = 112`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.114 `swap_card` (Action 113)

- **模块与动作标识**：`Mod = 2`, `Act = 113`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.115 `tian_di_yu_pai` (Action 114)

- **模块与动作标识**：`Mod = 2`, `Act = 114`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.122 `open_furnace` (Action 121)

- **模块与动作标识**：`Mod = 2`, `Act = 121`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.123 `drag_furnace_item` (Action 122)

- **模块与动作标识**：`Mod = 2`, `Act = 122`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.124 `get_yupai_info` (Action 123)

- **模块与动作标识**：`Mod = 2`, `Act = 123`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.125 `get_yupai_npc_item_list` (Action 124)

- **模块与动作标识**：`Mod = 2`, `Act = 124`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_1` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_2` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_3` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.126 `player_buy_yupai_npc_item` (Action 125)

- **模块与动作标识**：`Mod = 2`, `Act = 125`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.127 `get_gift_deciphe_key` (Action 126)

- **模块与动作标识**：`Mod = 2`, `Act = 126`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, str]` | 网络大端序编解码 |

### 2.128 `replace_player_role_equip` (Action 127)

- **模块与动作标识**：`Mod = 2`, `Act = 127`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Array[UByteUtil]` | `List[int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.129 `get_player_role_replace_info` (Action 128)

- **模块与动作标识**：`Mod = 2`, `Act = 128`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`22` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_17` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_18` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_19` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_20` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_21` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.130 `player_role_can_replace_info` (Action 129)

- **模块与动作标识**：`Mod = 2`, `Act = 129`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`22` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_5` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_6` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_7` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_8` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_9` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_10` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_11` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_12` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_13` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_14` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_15` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_16` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_17` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_18` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_19` | `ByteUtil` | `int` | 网络大端序编解码 |
  | `field_20` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_21` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.131 `large_use_grid_item` (Action 130)

- **模块与动作标识**：`Mod = 2`, `Act = 130`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.132 `use_set_nickname_item` (Action 131)

- **模块与动作标识**：`Mod = 2`, `Act = 131`
- **请求参数字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `StringUtil` | `str` | 网络大端序编解码 |
  | `field_2` | `UByteUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `StringUtil` | `str` | 网络大端序编解码 |

### 2.133 `use_set_role_item` (Action 132)

- **模块与动作标识**：`Mod = 2`, `Act = 132`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.134 `player_use_single_item` (Action 133)

- **模块与动作标识**：`Mod = 2`, `Act = 133`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.135 `notify_item_attr_plus` (Action 134)

- **模块与动作标识**：`Mod = 2`, `Act = 134`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`5` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_4` | `ShortUtil` | `int` | 网络大端序编解码 |

### 2.136 `get_player_home_warehouse_grids` (Action 135)

- **模块与动作标识**：`Mod = 2`, `Act = 135`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.137 `move_home_warehouse_grid_item_to_pack` (Action 136)

- **模块与动作标识**：`Mod = 2`, `Act = 136`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.138 `move_pack_grid_item_to_home_warehouse` (Action 137)

- **模块与动作标识**：`Mod = 2`, `Act = 137`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.149 `classify_home_warehouse` (Action 148)

- **模块与动作标识**：`Mod = 2`, `Act = 148`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.150 `change_home_warehouse_item_grid` (Action 149)

- **模块与动作标识**：`Mod = 2`, `Act = 149`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.151 `drop_home_warehouse_grid_item` (Action 150)

- **模块与动作标识**：`Mod = 2`, `Act = 150`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.152 `player_use_random_item` (Action 151)

- **模块与动作标识**：`Mod = 2`, `Act = 151`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.153 `get_player_supergift_warehouse_grids` (Action 152)

- **模块与动作标识**：`Mod = 2`, `Act = 152`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.154 `move_supergift_warehouse_grid_item_to_pack` (Action 153)

- **模块与动作标识**：`Mod = 2`, `Act = 153`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.155 `move_pack_grid_item_to_supergift_warehouse` (Action 154)

- **模块与动作标识**：`Mod = 2`, `Act = 154`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.156 `classify_supergift_warehouse` (Action 155)

- **模块与动作标识**：`Mod = 2`, `Act = 155`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.157 `change_supergift_warehouse_item_grid` (Action 156)

- **模块与动作标识**：`Mod = 2`, `Act = 156`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.158 `use_ding_ji_ji_neng_shu_zi_xuan_bao` (Action 157)

- **模块与动作标识**：`Mod = 2`, `Act = 157`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.159 `expand_page_two_grid` (Action 158)

- **模块与动作标识**：`Mod = 2`, `Act = 158`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.160 `player_use_grid_item_need_choose` (Action 159)

- **模块与动作标识**：`Mod = 2`, `Act = 159`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.161 `use_choose_box` (Action 160)

- **模块与动作标识**：`Mod = 2`, `Act = 160`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.162 `get_yun_niang_items` (Action 161)

- **模块与动作标识**：`Mod = 2`, `Act = 161`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(6)` | `Tuple[int, int, int, int, int, int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.163 `buy_yun_niang_item` (Action 162)

- **模块与动作标识**：`Mod = 2`, `Act = 162`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`4` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_3` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.164 `get_player_friendship_warehouse_grids` (Action 163)

- **模块与动作标识**：`Mod = 2`, `Act = 163`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_2` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.165 `move_friendship_warehouse_grid_item_to_pack` (Action 164)

- **模块与动作标识**：`Mod = 2`, `Act = 164`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.166 `move_pack_grid_item_to_friendship_warehouse` (Action 165)

- **模块与动作标识**：`Mod = 2`, `Act = 165`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.167 `classify_friendship_warehouse` (Action 166)

- **模块与动作标识**：`Mod = 2`, `Act = 166`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.168 `change_friendship_warehouse_item_grid` (Action 167)

- **模块与动作标识**：`Mod = 2`, `Act = 167`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.169 `drop_friendship_warehouse_grid_item` (Action 168)

- **模块与动作标识**：`Mod = 2`, `Act = 168`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.170 `player_refresh_grid_item_need_choose` (Action 169)

- **模块与动作标识**：`Mod = 2`, `Act = 169`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |

### 2.171 `player_batch_grid_item` (Action 170)

- **模块与动作标识**：`Mod = 2`, `Act = 170`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Array[IntUtil]` | `List[int]` | 网络大端序编解码 |
  | `field_2` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.172 `elixir_transform_panel` (Action 171)

- **模块与动作标识**：`Mod = 2`, `Act = 171`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`3` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(3)` | `Tuple[int, int, int]` | 网络大端序编解码 |
  | `field_2` | `IntUtil` | `int` | 网络大端序编解码 |

### 2.173 `elixir_transform` (Action 172)

- **模块与动作标识**：`Mod = 2`, `Act = 172`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.174 `get_pearl_privilege_info` (Action 173)

- **模块与动作标识**：`Mod = 2`, `Act = 173`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(5)` | `Tuple[int, int, int, int, int]` | 网络大端序编解码 |

### 2.175 `exchange_pearl_privilege` (Action 174)

- **模块与动作标识**：`Mod = 2`, `Act = 174`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(17)` | `Tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]` | 网络大端序编解码 |

### 2.176 `get_memory_item_info` (Action 175)

- **模块与动作标识**：`Mod = 2`, `Act = 175`
- **请求参数字段** (`0` 项):
  *(无入参)*

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `Tuple(2)` | `Tuple[int, int]` | 网络大端序编解码 |

### 2.177 `select_wish_box_type` (Action 176)

- **模块与动作标识**：`Mod = 2`, `Act = 176`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `ShortUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

### 2.178 `ming_wen_change_panel` (Action 177)

- **模块与动作标识**：`Mod = 2`, `Act = 177`
- **请求参数字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `Tuple(4)` | `Tuple[int, int, int, Tuple[int, int]]` | 网络大端序编解码 |

### 2.179 `ming_wen_change` (Action 178)

- **模块与动作标识**：`Mod = 2`, `Act = 178`
- **请求参数字段** (`2` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `IntUtil` | `int` | 网络大端序编解码 |
  | `field_1` | `IntUtil` | `int` | 网络大端序编解码 |

- **响应回包字段** (`1` 项):
  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |
  | :--- | :--- | :--- | :--- |
  | `field_0` | `UByteUtil` | `int` | 网络大端序编解码 |

---

## 3. Python 契约快速使用示例

```python
from protocol.contracts.mod_2_item import (
    ItemGetItemBasicalInfosReq,
    ItemGetItemBasicalInfosResp,
)

# 发起 Mod 2 业务请求
# req = ItemGetItemBasicalInfosReq(...)
# payload = req.encode_payload()
```

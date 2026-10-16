# 全域协议全景速查大表与 880 模块元数据库 (Protocol Index & Catalog)

> **文档状态**：已冻结 (Frozen)  
> **全量模块总数**：`880` 个官方独立业务模块  
> **全量动作总数**：`8719` 个网络指令动作  
> **全量常量总数**：`13765` 个状态与错误枚举常量  
> **元数据来源**：官方核心 Flash AVM2 字节码 (`block_0.abc`, 35.37 MB)  
> **机器可读索引**：`protocol/manifest/all_modules_manifest.json` (9.06 MB)  
> **CLI 生成器**：`python scripts/protocol_codegen.py --mod <ID>`  
> **关联工单**：[Ticket 3: 全量 879 模块 Manifest 元数据库提取与 CLI 按需代码生成器](https://github.com/atengk/sxd-bot/issues/4)  
> **上游规约**：[00_binary_framing_and_codecs.md](./00_binary_framing_and_codecs.md) | [01_micro_client_architecture_and_relay.md](./01_micro_client_architecture_and_relay.md)

---

## 1. 协议元数据库设计与按需生成体系

为彻底解决历史开发中“翻遍旧代码找协议号”、“边抓包边猜参数类型”、“跨模块重复逆向”的工程痛点，本项目建立了**全量元数据字典 (Single Source of Truth) + 按需即时代码生成 (On-Demand Codegen)** 架构：

1. **全景 Manifest 索引库**：`protocol/manifest/all_modules_manifest.json` 机器可读索引库记录了游戏中自 Mod 0 至 Mod 891 的全部 880 个协议模块的官方类名、数值编号、Action 列表与字段级类型；
2. **一键按需生成 CLI**：任何二次开发者或自动化任务，只需在终端输入命令：
   ```bash
   python scripts/protocol_codegen.py --mod 0
   # 或通过英文名称
   python scripts/protocol_codegen.py --name Town
   ```
   即可毫秒级生成强类型 Python `@dataclass` 契约代码与对应的 Markdown 技术规范文档，杜绝人工手写编解码器引入的格式或端序缺陷；
3. **分层精修架构**：高频基石玩法（如角色登录、城镇移动、精英副本、猎命药园）提供人工语义精修的强类型字段名称与卫语句防护；长尾与边缘玩法依赖 Manifest 与生成器按需扩充，实现 100% 官方全覆盖。

---

## 2. 核心领域模块全景速查表 (Top Tier Modules)

| 模块 ID | 模块名称 | 官方类名 | 动作数 | 常量数 | 代表性接口动作 (Actions) | 快速生成命令 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`0`** | `Player` | `Mod_Player_Base` | `69` | `124` | `login, player_first_init, get_player_info` | `python scripts/protocol_codegen.py --mod 0` |
| **`1`** | `Town` | `Mod_Town_Base` | `14` | `15` | `enter_town, leave_town, move_to` | `python scripts/protocol_codegen.py --mod 1` |
| **`2`** | `Item` | `Mod_Item_Base` | `113` | `231` | `get_item_basical_infos, get_empty_grid_number, get_all_player_item_infos` | `python scripts/protocol_codegen.py --mod 2` |
| **`3`** | `Quest` | `Mod_Quest_Base` | `17` | `18` | `npc_info_by_npcid, npc_info_by_questid, accept_quest` | `python scripts/protocol_codegen.py --mod 3` |
| **`4`** | `Mission` | `Mod_Mission_Base` | `27` | `49` | `get_sections, enter_mission, fight_monster` | `python scripts/protocol_codegen.py --mod 4` |
| **`5`** | `Role` | `Mod_Role_Base` | `18` | `20` | `get_town_player_info, get_role_list, down_partners` | `python scripts/protocol_codegen.py --mod 5` |
| **`6`** | `Chat` | `Mod_Chat_Base` | `18` | `32` | `chat_with_players, bro_to_players, disable_player_talk` | `python scripts/protocol_codegen.py --mod 6` |
| **`7`** | `Research` | `Mod_Research_Base` | `6` | `8` | `research_list, research_upgrade, clear_cd_time_show` | `python scripts/protocol_codegen.py --mod 7` |
| **`8`** | `Partners` | `Mod_Partners_Base` | `19` | `39` | `partners_list, partners_invite, now_and_next_Recommend_role_list` | `python scripts/protocol_codegen.py --mod 8` |
| **`9`** | `Friend` | `Mod_Friend_Base` | `21` | `26` | `add_friend, add_to_black, delete_friend` | `python scripts/protocol_codegen.py --mod 9` |
| **`10`** | `Faction` | `Mod_Faction_Base` | `55` | `87` | `found_faction, disband_faction, faction_request` | `python scripts/protocol_codegen.py --mod 10` |
| **`11`** | `Deploy` | `Mod_Deploy_Base` | `5` | `3` | `deploy_list, up_deploy, down_deploy` | `python scripts/protocol_codegen.py --mod 11` |
| **`12`** | `Training` | `Mod_Training_Base` | `4` | `12` | `panel_show, training, modify_role_data` | `python scripts/protocol_codegen.py --mod 12` |
| **`13`** | `Farm` | `Mod_Farm_Base` | `27` | `35` | `get_farmlandinfo_list, get_player_roleinfo_list, get_herbs_seed` | `python scripts/protocol_codegen.py --mod 13` |
| **`14`** | `MultipleMission` | `Mod_MultipleMission_Base` | `21` | `19` | `open_multiple_mission, get_multiple_mission_team_list, get_player_team_info` | `python scripts/protocol_codegen.py --mod 14` |
| **`15`** | `WorldSkyLanternBless` | `Mod_WorldSkyLanternBless_Base` | `14` | `38` | `get_activity_time, get_bless_rank, get_player_info` | `python scripts/protocol_codegen.py --mod 15` |
| **`16`** | `Rune` | `Mod_Rune_Base` | `7` | `5` | `rune_list, rune_use, batch_rune_list` | `python scripts/protocol_codegen.py --mod 16` |
| **`18`** | `Vip` | `Mod_Vip_Base` | `3` | `5` | `get_player_vip_info, get_send_gift, buy_send_gift` | `python scripts/protocol_codegen.py --mod 18` |
| **`19`** | `Pk` | `Mod_Pk_Base` | `2` | `0` | `start_war, get_player_war_report` | `python scripts/protocol_codegen.py --mod 19` |
| **`20`** | `Notify` | `Mod_Notify_Base` | `108` | `36` | `mission_award, pk_award, complete_reel_production` | `python scripts/protocol_codegen.py --mod 20` |
| **`21`** | `TravelEvent` | `Mod_TravelEvent_Base` | `5` | `11` | `get_activity_info, get_event_and_answer, answer_travel_event` | `python scripts/protocol_codegen.py --mod 21` |
| **`22`** | `Fate` | `Mod_Fate_Base` | `41` | `44` | `get_fate_npc, get_temp_fate, pickup_fate` | `python scripts/protocol_codegen.py --mod 22` |
| **`23`** | `CampWar` | `Mod_CampWar_Base` | `15` | `26` | `get_camp_open_time, open_camp_war, close_camp_war` | `python scripts/protocol_codegen.py --mod 23` |
| **`24`** | `WorldBoss` | `Mod_WorldBoss_Base` | `20` | `10` | `get_world_boss_list, get_world_boss_data, fight_world_boss` | `python scripts/protocol_codegen.py --mod 24` |
| **`25`** | `MissionPractice` | `Mod_MissionPractice_Base` | `9` | `8` | `get_practice_info, start_practice, cancel_practice` | `python scripts/protocol_codegen.py --mod 25` |
| **`26`** | `WarReport` | `Mod_WarReport_Base` | `1` | `0` | `record_war_report` | `python scripts/protocol_codegen.py --mod 26` |
| **`27`** | `Gm` | `Mod_Gm_Base` | `3` | `7` | `get_remain_submit_times, submit_bug, get_bug_list` | `python scripts/protocol_codegen.py --mod 27` |
| **`28`** | `SuperSport` | `Mod_SuperSport_Base` | `14` | `14` | `open_super_sport, get_challenge_list, start_challenge` | `python scripts/protocol_codegen.py --mod 28` |
| **`29`** | `FactionWar` | `Mod_FactionWar_Base` | `21` | `6` | `notify_status, get_faction_war_list, sign_up` | `python scripts/protocol_codegen.py --mod 29` |
| **`30`** | `TakeBible` | `Mod_TakeBible_Base` | `22` | `39` | `open_take_bible, close_take_bible, get_take_bible_info` | `python scripts/protocol_codegen.py --mod 30` |
| **`31`** | `SendFlower` | `Mod_SendFlower_Base` | `4` | `8` | `player_send_flower_info, send_player_flower, send_flower_ranking` | `python scripts/protocol_codegen.py --mod 31` |
| **`32`** | `Tower` | `Mod_Tower_Base` | `10` | `8` | `get_tower_info, start_challenge, reset_layer` | `python scripts/protocol_codegen.py --mod 32` |
| **`33`** | `Inherit` | `Mod_Inherit_Base` | `4` | `7` | `role_list, role_attribute, attribute_after_inherit` | `python scripts/protocol_codegen.py --mod 33` |
| **`34`** | `SealSoul` | `Mod_SealSoul_Base` | `32` | `23` | `soul_info_by_location, swap_soul, move_soul` | `python scripts/protocol_codegen.py --mod 34` |
| **`35`** | `HeroMission` | `Mod_HeroMission_Base` | `10` | `11` | `get_hero_mission_list, buy_hero_challenge, start_practice` | `python scripts/protocol_codegen.py --mod 35` |
| **`36`** | `ServerWar` | `Mod_ServerWar_Base` | `17` | `56` | `get_race_step, get_standings, get_race_list` | `python scripts/protocol_codegen.py --mod 36` |
| **`37`** | `Dujie` | `Mod_Dujie_Base` | `5` | `12` | `dujie_info, add_player_role_state_point, role_list` | `python scripts/protocol_codegen.py --mod 37` |
| **`38`** | `RollCake` | `Mod_RollCake_Base` | `7` | `6` | `roll, get_count, reroll` | `python scripts/protocol_codegen.py --mod 38` |
| **`39`** | `Achievement` | `Mod_Achievement_Base` | `6` | `6` | `get_player_achievement_list, notify_complete_achievement, fate_achievement_completed` | `python scripts/protocol_codegen.py --mod 39` |
| **`40`** | `GetPeach` | `Mod_GetPeach_Base` | `6` | `6` | `get_peach, buy_monkeys, peach_info` | `python scripts/protocol_codegen.py --mod 40` |
| **`41`** | `WorshipMars` | `Mod_WorshipMars_Base` | `6` | `8` | `mars_info, incense, get_blessing_times_and_exp_add` | `python scripts/protocol_codegen.py --mod 41` |
| **`42`** | `HeroesWar` | `Mod_HeroesWar_Base` | `19` | `29` | `get_heroes_open_time, open_heroes_war, close_heroes_war` | `python scripts/protocol_codegen.py --mod 42` |
| **`43`** | `RedEnvelopes` | `Mod_RedEnvelopes_Base` | `3` | `5` | `get_envelopes_info, get_envelope, get_date` | `python scripts/protocol_codegen.py --mod 43` |
| **`44`** | `Zodiac` | `Mod_Zodiac_Base` | `3` | `8` | `zodiac_info, challenge, exchange_stone` | `python scripts/protocol_codegen.py --mod 44` |
| **`45`** | `Practice` | `Mod_Practice_Base` | `2` | `3` | `quickly, quickly_all` | `python scripts/protocol_codegen.py --mod 45` |
| **`46`** | `SuperDeploy` | `Mod_SuperDeploy_Base` | `18` | `18` | `super_deploy_list, up_deploy, down_deploy` | `python scripts/protocol_codegen.py --mod 46` |
| **`47`** | `StudyStunt` | `Mod_StudyStunt_Base` | `6` | `11` | `player_stunt_info, player_study_stunt, player_use_role_stunt_id` | `python scripts/protocol_codegen.py --mod 47` |
| **`48`** | `PetAnimal` | `Mod_PetAnimal_Base` | `4` | `8` | `pet_animal_info, change_name, feed_pet_animal` | `python scripts/protocol_codegen.py --mod 48` |
| **`49`** | `WorldFactionWar` | `Mod_WorldFactionWar_Base` | `18` | `34` | `get_race_step, get_race_list, get_war_result_list` | `python scripts/protocol_codegen.py --mod 49` |
| **`50`** | `DreamSection` | `Mod_DreamSection_Base` | `4` | `8` | `get_player_dream_section_info, challenge_section, recruit_partner` | `python scripts/protocol_codegen.py --mod 50` |
| **`51`** | `CatHunt` | `Mod_CatHunt_Base` | `2` | `21` | `auto_search_bonus, use_map_search` | `python scripts/protocol_codegen.py --mod 51` |
| **`52`** | `Assistant` | `Mod_Assistant_Base` | `4` | `8` | `info, get_award, complete_number` | `python scripts/protocol_codegen.py --mod 52` |
| **`53`** | `HaloRole` | `Mod_HaloRole_Base` | `2` | `6` | `get_challenge_info, start_challenge` | `python scripts/protocol_codegen.py --mod 53` |
| **`54`** | `Furnace` | `Mod_Furnace_Base` | `6` | `25` | `player_role_info, make_favor_item, submit_favor_item` | `python scripts/protocol_codegen.py --mod 54` |
| **`56`** | `WeekRanking` | `Mod_WeekRanking_Base` | `3` | `4` | `get_week_ranking, get_week_ranking_first_player, notify_week_ranking_type` | `python scripts/protocol_codegen.py --mod 56` |
| **`57`** | `BeelzebubTrials` | `Mod_BeelzebubTrials_Base` | `28` | `34` | `get_beelzebub_trials_open_time, open_beelzebub_trials, get_beelzebub_trials_team_list` | `python scripts/protocol_codegen.py --mod 57` |
| **`58`** | `NineRegions` | `Mod_NineRegions_Base` | `33` | `39` | `open_panel, start_challenge, get_player_bless_level` | `python scripts/protocol_codegen.py --mod 58` |
| **`63`** | `FingerGuess` | `Mod_FingerGuess_Base` | `6` | `11` | `finger_guess_state, enter_room, fight` | `python scripts/protocol_codegen.py --mod 63` |
| **`64`** | `DuanWu` | `Mod_DuanWu_Base` | `4` | `8` | `zongzi_state, get_zongzi, worship_state` | `python scripts/protocol_codegen.py --mod 64` |
| **`65`** | `TopWar` | `Mod_TopWar_Base` | `21` | `22` | `open_top_war, close_top_war, create_team` | `python scripts/protocol_codegen.py --mod 65` |

---

## 3. 全量 880 模块完整字母与编号索引矩阵 (Full Index Matrix)

以下为全量官方 880 个协议模块按数值编号索引总览（支持全文搜索或通过脚本按需拉取）：

| 模块 ID | 模块名称 (`com.protocols::*`) | 动作总数 | 示例动作 (Sample Actions) | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| `0` | `Mod_Player_Base` | `69` | `login, player_first_init` | `[READY_IN_MANIFEST]` |
| `1` | `Mod_Town_Base` | `14` | `enter_town, leave_town` | `[READY_IN_MANIFEST]` |
| `2` | `Mod_Item_Base` | `113` | `get_item_basical_infos, get_empty_grid_number` | `[READY_IN_MANIFEST]` |
| `3` | `Mod_Quest_Base` | `17` | `npc_info_by_npcid, npc_info_by_questid` | `[READY_IN_MANIFEST]` |
| `4` | `Mod_Mission_Base` | `27` | `get_sections, enter_mission` | `[READY_IN_MANIFEST]` |
| `5` | `Mod_Role_Base` | `18` | `get_town_player_info, get_role_list` | `[READY_IN_MANIFEST]` |
| `6` | `Mod_Chat_Base` | `18` | `chat_with_players, bro_to_players` | `[READY_IN_MANIFEST]` |
| `7` | `Mod_Research_Base` | `6` | `research_list, research_upgrade` | `[READY_IN_MANIFEST]` |
| `8` | `Mod_Partners_Base` | `19` | `partners_list, partners_invite` | `[READY_IN_MANIFEST]` |
| `9` | `Mod_Friend_Base` | `21` | `add_friend, add_to_black` | `[READY_IN_MANIFEST]` |
| `10` | `Mod_Faction_Base` | `55` | `found_faction, disband_faction` | `[READY_IN_MANIFEST]` |
| `11` | `Mod_Deploy_Base` | `5` | `deploy_list, up_deploy` | `[READY_IN_MANIFEST]` |
| `12` | `Mod_Training_Base` | `4` | `panel_show, training` | `[READY_IN_MANIFEST]` |
| `13` | `Mod_Farm_Base` | `27` | `get_farmlandinfo_list, get_player_roleinfo_list` | `[READY_IN_MANIFEST]` |
| `14` | `Mod_MultipleMission_Base` | `21` | `open_multiple_mission, get_multiple_mission_team_list` | `[READY_IN_MANIFEST]` |
| `15` | `Mod_WorldSkyLanternBless_Base` | `14` | `get_activity_time, get_bless_rank` | `[READY_IN_MANIFEST]` |
| `16` | `Mod_Rune_Base` | `7` | `rune_list, rune_use` | `[READY_IN_MANIFEST]` |
| `18` | `Mod_Vip_Base` | `3` | `get_player_vip_info, get_send_gift` | `[READY_IN_MANIFEST]` |
| `19` | `Mod_Pk_Base` | `2` | `start_war, get_player_war_report` | `[READY_IN_MANIFEST]` |
| `20` | `Mod_Notify_Base` | `108` | `mission_award, pk_award` | `[READY_IN_MANIFEST]` |
| `21` | `Mod_TravelEvent_Base` | `5` | `get_activity_info, get_event_and_answer` | `[READY_IN_MANIFEST]` |
| `22` | `Mod_Fate_Base` | `41` | `get_fate_npc, get_temp_fate` | `[READY_IN_MANIFEST]` |
| `23` | `Mod_CampWar_Base` | `15` | `get_camp_open_time, open_camp_war` | `[READY_IN_MANIFEST]` |
| `24` | `Mod_WorldBoss_Base` | `20` | `get_world_boss_list, get_world_boss_data` | `[READY_IN_MANIFEST]` |
| `25` | `Mod_MissionPractice_Base` | `9` | `get_practice_info, start_practice` | `[READY_IN_MANIFEST]` |
| `26` | `Mod_WarReport_Base` | `1` | `record_war_report` | `[READY_IN_MANIFEST]` |
| `27` | `Mod_Gm_Base` | `3` | `get_remain_submit_times, submit_bug` | `[READY_IN_MANIFEST]` |
| `28` | `Mod_SuperSport_Base` | `14` | `open_super_sport, get_challenge_list` | `[READY_IN_MANIFEST]` |
| `29` | `Mod_FactionWar_Base` | `21` | `notify_status, get_faction_war_list` | `[READY_IN_MANIFEST]` |
| `30` | `Mod_TakeBible_Base` | `22` | `open_take_bible, close_take_bible` | `[READY_IN_MANIFEST]` |
| `31` | `Mod_SendFlower_Base` | `4` | `player_send_flower_info, send_player_flower` | `[READY_IN_MANIFEST]` |
| `32` | `Mod_Tower_Base` | `10` | `get_tower_info, start_challenge` | `[READY_IN_MANIFEST]` |
| `33` | `Mod_Inherit_Base` | `4` | `role_list, role_attribute` | `[READY_IN_MANIFEST]` |
| `34` | `Mod_SealSoul_Base` | `32` | `soul_info_by_location, swap_soul` | `[READY_IN_MANIFEST]` |
| `35` | `Mod_HeroMission_Base` | `10` | `get_hero_mission_list, buy_hero_challenge` | `[READY_IN_MANIFEST]` |
| `36` | `Mod_ServerWar_Base` | `17` | `get_race_step, get_standings` | `[READY_IN_MANIFEST]` |
| `37` | `Mod_Dujie_Base` | `5` | `dujie_info, add_player_role_state_point` | `[READY_IN_MANIFEST]` |
| `38` | `Mod_RollCake_Base` | `7` | `roll, get_count` | `[READY_IN_MANIFEST]` |
| `39` | `Mod_Achievement_Base` | `6` | `get_player_achievement_list, notify_complete_achievement` | `[READY_IN_MANIFEST]` |
| `40` | `Mod_GetPeach_Base` | `6` | `get_peach, buy_monkeys` | `[READY_IN_MANIFEST]` |
| `41` | `Mod_WorshipMars_Base` | `6` | `mars_info, incense` | `[READY_IN_MANIFEST]` |
| `42` | `Mod_HeroesWar_Base` | `19` | `get_heroes_open_time, open_heroes_war` | `[READY_IN_MANIFEST]` |
| `43` | `Mod_RedEnvelopes_Base` | `3` | `get_envelopes_info, get_envelope` | `[READY_IN_MANIFEST]` |
| `44` | `Mod_Zodiac_Base` | `3` | `zodiac_info, challenge` | `[READY_IN_MANIFEST]` |
| `45` | `Mod_Practice_Base` | `2` | `quickly, quickly_all` | `[READY_IN_MANIFEST]` |
| `46` | `Mod_SuperDeploy_Base` | `18` | `super_deploy_list, up_deploy` | `[READY_IN_MANIFEST]` |
| `47` | `Mod_StudyStunt_Base` | `6` | `player_stunt_info, player_study_stunt` | `[READY_IN_MANIFEST]` |
| `48` | `Mod_PetAnimal_Base` | `4` | `pet_animal_info, change_name` | `[READY_IN_MANIFEST]` |
| `49` | `Mod_WorldFactionWar_Base` | `18` | `get_race_step, get_race_list` | `[READY_IN_MANIFEST]` |
| `50` | `Mod_DreamSection_Base` | `4` | `get_player_dream_section_info, challenge_section` | `[READY_IN_MANIFEST]` |
| `51` | `Mod_CatHunt_Base` | `2` | `auto_search_bonus, use_map_search` | `[READY_IN_MANIFEST]` |
| `52` | `Mod_Assistant_Base` | `4` | `info, get_award` | `[READY_IN_MANIFEST]` |
| `53` | `Mod_HaloRole_Base` | `2` | `get_challenge_info, start_challenge` | `[READY_IN_MANIFEST]` |
| `54` | `Mod_Furnace_Base` | `6` | `player_role_info, make_favor_item` | `[READY_IN_MANIFEST]` |
| `56` | `Mod_WeekRanking_Base` | `3` | `get_week_ranking, get_week_ranking_first_player` | `[READY_IN_MANIFEST]` |
| `57` | `Mod_BeelzebubTrials_Base` | `28` | `get_beelzebub_trials_open_time, open_beelzebub_trials` | `[READY_IN_MANIFEST]` |
| `58` | `Mod_NineRegions_Base` | `33` | `open_panel, start_challenge` | `[READY_IN_MANIFEST]` |
| `63` | `Mod_FingerGuess_Base` | `6` | `finger_guess_state, enter_room` | `[READY_IN_MANIFEST]` |
| `64` | `Mod_DuanWu_Base` | `4` | `zongzi_state, get_zongzi` | `[READY_IN_MANIFEST]` |
| `65` | `Mod_TopWar_Base` | `21` | `open_top_war, close_top_war` | `[READY_IN_MANIFEST]` |
| `66` | `Mod_NewTopWar_Base` | `40` | `create_team, disband_team` | `[READY_IN_MANIFEST]` |
| `67` | `Mod_SpecialPartner_Base` | `4` | `get_partner_info, get_mission_award` | `[READY_IN_MANIFEST]` |
| `68` | `Mod_FindImmortal_Base` | `13` | `open_find_immortal, start_find_immortal` | `[READY_IN_MANIFEST]` |
| `69` | `Mod_LuckyWheel_Base` | `2` | `open_lucky_wheel, start_lucky_wheel` | `[READY_IN_MANIFEST]` |
| `70` | `Mod_FactionMonster_Base` | `9` | `get_status, get_monster_info` | `[READY_IN_MANIFEST]` |
| `71` | `Mod_ServerFactionWar_Base` | `10` | `get_race_step, get_standings` | `[READY_IN_MANIFEST]` |
| `72` | `Mod_Sigil_Base` | `6` | `player_sigil_info, upgrade` | `[READY_IN_MANIFEST]` |
| `73` | `Mod_Adventure_Base` | `18` | `get_adventure_open_time, open_adventure` | `[READY_IN_MANIFEST]` |
| `74` | `Mod_IngotLuckWheel_Base` | `3` | `get_consume_ingot, exchange_gift` | `[READY_IN_MANIFEST]` |
| `75` | `Mod_SealDemon_Base` | `24` | `get_seal_demon_open_time, open_seal_demon` | `[READY_IN_MANIFEST]` |
| `76` | `Mod_Dance_Base` | `6` | `get_dance_info, start_dance` | `[READY_IN_MANIFEST]` |
| `77` | `Mod_Equipment_Base` | `27` | `get_player_role_exclusive_artifact_info, make_exclusive_artifact` | `[READY_IN_MANIFEST]` |
| `78` | `Mod_UproarHeaven_Base` | `4` | `palace_info, palace_monster_info` | `[READY_IN_MANIFEST]` |
| `79` | `Mod_LionKing_Base` | `23` | `lion_king_status, sign_faction_list` | `[READY_IN_MANIFEST]` |
| `80` | `Mod_Rulai_Base` | `4` | `get_rulai_info, player_rulai_incense` | `[READY_IN_MANIFEST]` |
| `81` | `Mod_BuyActivity_Base` | `3` | `is_activity_time, get_activity_info` | `[READY_IN_MANIFEST]` |
| `82` | `Mod_FarmActivity_Base` | `5` | `info, get_award` | `[READY_IN_MANIFEST]` |
| `83` | `Mod_ChristmasActivity_Base` | `5` | `info, get_award` | `[READY_IN_MANIFEST]` |
| `84` | `Mod_Mount_Base` | `16` | `get_player_mount_list, update_mount_transport` | `[READY_IN_MANIFEST]` |
| `85` | `Mod_Library_Base` | `8` | `get_library_info, up_library_level` | `[READY_IN_MANIFEST]` |
| `86` | `Mod_LanternFestival_Base` | `5` | `info, get_award` | `[READY_IN_MANIFEST]` |
| `87` | `Mod_LuckyStore_Base` | `21` | `get_super_box_get_time_and_statu, open_super_box` | `[READY_IN_MANIFEST]` |
| `88` | `Mod_OldPlayer_Base` | `7` | `get_activity_info, get_old_player_info` | `[READY_IN_MANIFEST]` |
| `89` | `Mod_SignIn_Base` | `6` | `get_sign_in_info, get_continue_award` | `[READY_IN_MANIFEST]` |
| `90` | `Mod_TwinDragons_Base` | `32` | `get_player_twin_dragons_team, get_all_twin_dragons_team` | `[READY_IN_MANIFEST]` |
| `91` | `Mod_StYiZhanDaoDiPointRace_Base` | `25` | `join_yizhan, get_compititor` | `[READY_IN_MANIFEST]` |
| `92` | `Mod_SignInTwo_Base` | `7` | `get_player_sign_in_info_two, get_ji_and_ma_two` | `[READY_IN_MANIFEST]` |
| `93` | `Mod_SimpleActivity_Base` | `2` | `check_activity_award, fetch_activity_award` | `[READY_IN_MANIFEST]` |
| `94` | `Mod_StLogin_Base` | `1` | `login` | `[READY_IN_MANIFEST]` |
| `95` | `Mod_StTown_Base` | `12` | `enter_town, notify_enter_town` | `[READY_IN_MANIFEST]` |
| `96` | `Mod_StcLogin_Base` | `7` | `get_login_info, get_status` | `[READY_IN_MANIFEST]` |
| `97` | `Mod_StVoting_Base` | `2` | `get_voting_info, voting` | `[READY_IN_MANIFEST]` |
| `98` | `Mod_StWorldBoss_Base` | `21` | `get_st_world_boss_panel_info, get_st_boss_detect_info` | `[READY_IN_MANIFEST]` |
| `100` | `Mod_Mobile_Base` | `193` | `assistant_login, get_player_info` | `[READY_IN_MANIFEST]` |
| `101` | `Mod_Supernatural_Base` | `12` | `get_supernatural_info, up_supernatural_level` | `[READY_IN_MANIFEST]` |
| `102` | `Mod_ImmortalFantasy_Base` | `11` | `get_fantasy_stage_challenge_info, do_paper_scissors_and_stone` | `[READY_IN_MANIFEST]` |
| `103` | `Mod_FurnacePartner_Base` | `11` | `get_furnace_partner_info, upgrade_earch_goblin_level` | `[READY_IN_MANIFEST]` |
| `104` | `Mod_Nimbus_Base` | `2` | `nimbus_info, gather_nimbus` | `[READY_IN_MANIFEST]` |
| `105` | `Mod_HuntDemon_Base` | `2` | `open_hunt_demon, hunt_demon` | `[READY_IN_MANIFEST]` |
| `106` | `Mod_WorldPk_Base` | `7` | `get_status, get_panel_data` | `[READY_IN_MANIFEST]` |
| `107` | `Mod_StQiXi_Base` | `12` | `start_qi_xi, give_answer_and_award` | `[READY_IN_MANIFEST]` |
| `108` | `Mod_CircleWar_Base` | `2` | `circlewar_info, challenge` | `[READY_IN_MANIFEST]` |
| `109` | `Mod_StTower_Base` | `25` | `get_st_tower_open_time, open_st_tower` | `[READY_IN_MANIFEST]` |
| `110` | `Mod_Agate_Base` | `2` | `agate_list, agate_use` | `[READY_IN_MANIFEST]` |
| `111` | `Mod_Dragonball_Base` | `32` | `get_tmp_dragonball_basic_info, collect_dragonball` | `[READY_IN_MANIFEST]` |
| `112` | `Mod_Gamable_Base` | `8` | `get_gamable_info, bet` | `[READY_IN_MANIFEST]` |
| `113` | `Mod_StRulai_Base` | `4` | `get_rulai_info, player_rulai_incense` | `[READY_IN_MANIFEST]` |
| `114` | `Mod_StTakeBible_Base` | `24` | `open_take_bible, close_take_bible` | `[READY_IN_MANIFEST]` |
| `115` | `Mod_StSuperSport_Base` | `27` | `get_st_super_sport_status, get_player_st_super_sport` | `[READY_IN_MANIFEST]` |
| `116` | `Mod_Bloodline_Base` | `26` | `get_bloodline_info, awaken_bloodline` | `[READY_IN_MANIFEST]` |
| `117` | `Mod_StPracticeRoom_Base` | `18` | `get_rooms, get_room_info` | `[READY_IN_MANIFEST]` |
| `118` | `Mod_GodWar_Base` | `31` | `get_god_war_status, sign_up_god_war` | `[READY_IN_MANIFEST]` |
| `119` | `Mod_StXianFuSup_Base` | `20` | `open, sign_up` | `[READY_IN_MANIFEST]` |
| `121` | `Mod_AutoActivity_Base` | `7` | `auto_activity_info, set_auto_activity` | `[READY_IN_MANIFEST]` |
| `122` | `Mod_SkyLanternBless_Base` | `11` | `get_activity_time, get_bless_rank` | `[READY_IN_MANIFEST]` |
| `123` | `Mod_SpaceFind_Base` | `15` | `open_space_find, do_space_find` | `[READY_IN_MANIFEST]` |
| `124` | `Mod_ChaosEquipment_Base` | `25` | `get_pack_chaos_monster_list, get_role_chaos_monster_list` | `[READY_IN_MANIFEST]` |
| `125` | `Mod_StFightCard_Base` | `11` | `get_enemys, get_beaten_list` | `[READY_IN_MANIFEST]` |
| `126` | `Mod_StTravelShop_Base` | `3` | `travel_shop_info, buy_goods` | `[READY_IN_MANIFEST]` |
| `127` | `Mod_FunctionEnd_Base` | `5` | `is_game_function_end, game_function_end_gift` | `[READY_IN_MANIFEST]` |
| `128` | `Mod_WinterMission_Base` | `9` | `enter_mission, get_ranking` | `[READY_IN_MANIFEST]` |
| `129` | `Mod_StEightImmortals_Base` | `11` | `get_finished_missions, enter_mission` | `[READY_IN_MANIFEST]` |
| `130` | `Mod_ChristmasHuntDemon_Base` | `9` | `open_christmas_hunt_demon, close_christmas_hunt_demon` | `[READY_IN_MANIFEST]` |
| `131` | `Mod_MagicArms_Base` | `17` | `buy_magic_arms, equip_magic_arms` | `[READY_IN_MANIFEST]` |
| `132` | `Mod_StDaoyuanShop_Base` | `3` | `daoyuan_shop_item_list, buy_daoyuan_shop_item` | `[READY_IN_MANIFEST]` |
| `133` | `Mod_NewYearDaySignIn_Base` | `5` | `get_player_sign_in_info, get_sign_in_status` | `[READY_IN_MANIFEST]` |
| `134` | `Mod_BecomeImmortal_Base` | `9` | `get_become_immortal_data, update_become_immortal` | `[READY_IN_MANIFEST]` |
| `135` | `Mod_FairyTree_Base` | `7` | `is_fairy_tree_open, open_fairy_tree` | `[READY_IN_MANIFEST]` |
| `136` | `Mod_StChallenge_Base` | `11` | `get_player_st_challenge_info, customizing_info` | `[READY_IN_MANIFEST]` |
| `137` | `Mod_StLionKing_Base` | `28` | `lion_king_status, join_match` | `[READY_IN_MANIFEST]` |
| `138` | `Mod_Abnormal_Base` | `1` | `notify_warning` | `[READY_IN_MANIFEST]` |
| `139` | `Mod_GoldenDan_Base` | `10` | `get_player_golden_dan_list, get_player_golden_dan` | `[READY_IN_MANIFEST]` |
| `140` | `Mod_LotusLamp_Base` | `6` | `get_activity_time, enter_activity` | `[READY_IN_MANIFEST]` |
| `141` | `Mod_TempWarehouse_Base` | `4` | `get_item_list, pickup_item_to_package` | `[READY_IN_MANIFEST]` |
| `142` | `Mod_ChatWish_Base` | `2` | `get_key_word, chat_with_key_word` | `[READY_IN_MANIFEST]` |
| `143` | `Mod_Td_Base` | `11` | `get_race_players, enter` | `[READY_IN_MANIFEST]` |
| `144` | `Mod_OrangeEquipment_Base` | `19` | `get_player_pack_orange_equipment_list, equip_player_role` | `[READY_IN_MANIFEST]` |
| `145` | `Mod_WishTree_Base` | `14` | `get_wish_tree_info, get_player_wish_cost` | `[READY_IN_MANIFEST]` |
| `146` | `Mod_LendRole_Base` | `11` | `get_activity_info, friend_list` | `[READY_IN_MANIFEST]` |
| `147` | `Mod_StRichMan_Base` | `26` | `get_st_rich_man_status, join_st_rich_man` | `[READY_IN_MANIFEST]` |
| `148` | `Mod_MissionReelExchange_Base` | `2` | `get_reel_exchange_detail, buy_reel` | `[READY_IN_MANIFEST]` |
| `149` | `Mod_PanTaoActivity_Base` | `9` | `get_activity_state, notify` | `[READY_IN_MANIFEST]` |
| `150` | `Mod_Turnplate_Base` | `9` | `get_turnplate_status, get_player_turnplate` | `[READY_IN_MANIFEST]` |
| `151` | `Mod_ThreeAnniversarySignIn_Base` | `4` | `get_player_sign_in_info, get_sign_in_status` | `[READY_IN_MANIFEST]` |
| `152` | `Mod_RoleUpgrade_Base` | `6` | `role_upgrade_info, active_upgrade` | `[READY_IN_MANIFEST]` |
| `153` | `Mod_StShouChongActivity_Base` | `7` | `get_activity_state, notify` | `[READY_IN_MANIFEST]` |
| `154` | `Mod_Groupon_Base` | `8` | `get_groupon_status, get_groupon_info` | `[READY_IN_MANIFEST]` |
| `155` | `Mod_ChargeBack_Base` | `11` | `open_charge_back, get_gift` | `[READY_IN_MANIFEST]` |
| `157` | `Mod_TopLineup_Base` | `14` | `deploy_info, change_deploy` | `[READY_IN_MANIFEST]` |
| `158` | `Mod_PlayerNpc_Base` | `3` | `total_ingot_info, player_npc_info` | `[READY_IN_MANIFEST]` |
| `159` | `Mod_AttackCity_Base` | `35` | `get_attack_city_race_info, is_player_apply` | `[READY_IN_MANIFEST]` |
| `160` | `Mod_CardMaster_Base` | `16` | `get_card_master_status, get_player_card_master_info` | `[READY_IN_MANIFEST]` |
| `161` | `Mod_GiftItemPack_Base` | `3` | `get_item_list, pickup_item_to_package` | `[READY_IN_MANIFEST]` |
| `162` | `Mod_StZhaoCha_Base` | `13` | `get_st_zhao_cha_status, join_st_zhao_cha` | `[READY_IN_MANIFEST]` |
| `163` | `Mod_WorldCupGuess_Base` | `11` | `get_world_cup_guess_status, get_player_world_cup_guess_info` | `[READY_IN_MANIFEST]` |
| `164` | `Mod_WorldAnswer_Base` | `3` | `notify_answer_will_begin_after_one_minute, notify_question` | `[READY_IN_MANIFEST]` |
| `165` | `Mod_DayToDayWork_Base` | `10` | `get_act_info, get_quest_list` | `[READY_IN_MANIFEST]` |
| `166` | `Mod_CallOfBoss_Base` | `5` | `get_activity_state, notify` | `[READY_IN_MANIFEST]` |
| `167` | `Mod_Sudhana_Base` | `4` | `get_sudhana_status, get_player_sudhana_info` | `[READY_IN_MANIFEST]` |
| `168` | `Mod_FiveElements_Base` | `17` | `get_pack_five_elements_equip_list, get_role_five_elements` | `[READY_IN_MANIFEST]` |
| `169` | `Mod_UnlimitChallenge_Base` | `7` | `player_unlimit_challenge_info, monster_deploy_info` | `[READY_IN_MANIFEST]` |
| `170` | `Mod_FlopGame_Base` | `8` | `get_activity_state, notify` | `[READY_IN_MANIFEST]` |
| `171` | `Mod_GridGame_Base` | `4` | `get_grid_game_status, player_grid_game_info` | `[READY_IN_MANIFEST]` |
| `172` | `Mod_Laba_Base` | `5` | `laba_info, draw` | `[READY_IN_MANIFEST]` |
| `173` | `Mod_ShuiLuDaHui_Base` | `20` | `sign_up, get_player_shui_lu` | `[READY_IN_MANIFEST]` |
| `174` | `Mod_StRanking_Base` | `2` | `get_st_ranking, get_have_award_st_ranking` | `[READY_IN_MANIFEST]` |
| `175` | `Mod_Bank_Base` | `5` | `get_bank_activity_time, get_activity_info` | `[READY_IN_MANIFEST]` |
| `176` | `Mod_Scratch_Base` | `8` | `scratch_info, get_card` | `[READY_IN_MANIFEST]` |
| `178` | `Mod_StUnion_Base` | `31` | `get_st_union_list, get_request_st_union_list` | `[READY_IN_MANIFEST]` |
| `179` | `Mod_StUnionActivity_Base` | `10` | `get_st_union_tree_info, choose_wish_item` | `[READY_IN_MANIFEST]` |
| `180` | `Mod_CumulativeActivity_Base` | `8` | `get_cumulative_login_info, get_player_cumulative_login` | `[READY_IN_MANIFEST]` |
| `181` | `Mod_StUnionWar_Base` | `21` | `notify_status, get_player_st_union_war_status` | `[READY_IN_MANIFEST]` |
| `182` | `Mod_MonthCard_Base` | `18` | `month_card_info, buy_month_card` | `[READY_IN_MANIFEST]` |
| `183` | `Mod_StUnionMagic_Base` | `2` | `get_st_union_magic_list, upgrade` | `[READY_IN_MANIFEST]` |
| `184` | `Mod_Parkour_Base` | `7` | `get_active_info, start_run` | `[READY_IN_MANIFEST]` |
| `185` | `Mod_ScratchCard_Base` | `9` | `scratch_card_info, shave_card` | `[READY_IN_MANIFEST]` |
| `186` | `Mod_FruitMachine_Base` | `5` | `get_activity_info, get_player_score` | `[READY_IN_MANIFEST]` |
| `187` | `Mod_CardSoul_Base` | `13` | `get_card_info, active_card` | `[READY_IN_MANIFEST]` |
| `188` | `Mod_FindTreasure_Base` | `11` | `activity_info, open_find_treasure` | `[READY_IN_MANIFEST]` |
| `189` | `Mod_StRuins_Base` | `10` | `st_ruins_info, find_scrap` | `[READY_IN_MANIFEST]` |
| `190` | `Mod_StFlyingChessActivity_Base` | `16` | `get_player_info, join_match` | `[READY_IN_MANIFEST]` |
| `191` | `Mod_StUnionTrials_Base` | `15` | `get_activity_info, get_team_info_list` | `[READY_IN_MANIFEST]` |
| `192` | `Mod_ScoreGame_Base` | `8` | `get_activity_time, open_score_game` | `[READY_IN_MANIFEST]` |
| `193` | `Mod_StUnionShop_Base` | `2` | `get_shop_info, exchange` | `[READY_IN_MANIFEST]` |
| `194` | `Mod_ActivityGame_Base` | `27` | `get_activity_time, open_activity_game` | `[READY_IN_MANIFEST]` |
| `195` | `Mod_StAnswer_Base` | `4` | `get_activity_info, start_answer` | `[READY_IN_MANIFEST]` |
| `196` | `Mod_Painkiller_Base` | `10` | `new_time_occur, fight` | `[READY_IN_MANIFEST]` |
| `197` | `Mod_Matual_Base` | `12` | `friend_list, matual_info` | `[READY_IN_MANIFEST]` |
| `198` | `Mod_ForbiddenArea_Base` | `2` | `get_player_info, fight` | `[READY_IN_MANIFEST]` |
| `199` | `Mod_Awake_Base` | `34` | `player_skill_book_info, player_skill_book_pack` | `[READY_IN_MANIFEST]` |
| `200` | `Mod_StMobile_Base` | `48` | `get_st_login_info, st_login` | `[READY_IN_MANIFEST]` |
| `201` | `Mod_NewServerLoginAct_Base` | `3` | `is_can_join_activity, activity_info` | `[READY_IN_MANIFEST]` |
| `202` | `Mod_ShenGun_Base` | `4` | `shen_gun_info, all_server_shen_gun_count` | `[READY_IN_MANIFEST]` |
| `203` | `Mod_SuperPrizePool_Base` | `10` | `get_activity_info, get_player_info` | `[READY_IN_MANIFEST]` |
| `204` | `Mod_RockGame_Base` | `5` | `get_rock_game_status, player_rock_game` | `[READY_IN_MANIFEST]` |
| `205` | `Mod_StTrials_Base` | `7` | `active_info, mode_status` | `[READY_IN_MANIFEST]` |
| `206` | `Mod_Marry_Base` | `38` | `is_self_be_marry, get_player_marry_status` | `[READY_IN_MANIFEST]` |
| `207` | `Mod_Jewel_Base` | `9` | `get_pack_jewel_list, get_player_jewel_scrap` | `[READY_IN_MANIFEST]` |
| `208` | `Mod_ChristmasSock_Base` | `4` | `activity_info, hang_sock` | `[READY_IN_MANIFEST]` |
| `209` | `Mod_PassScoreGame_Base` | `4` | `get_player_info, get_award` | `[READY_IN_MANIFEST]` |
| `210` | `Mod_MarryHome_Base` | `20` | `get_self_home_info, buy_home` | `[READY_IN_MANIFEST]` |
| `211` | `Mod_MarryMoonOldShop_Base` | `2` | `buy_moon_shop_item, get_bought_list` | `[READY_IN_MANIFEST]` |
| `212` | `Mod_Courtyard_Base` | `21` | `get_player_info, watering` | `[READY_IN_MANIFEST]` |
| `213` | `Mod_StSnatchTreasure_Base` | `13` | `is_open, get_info` | `[READY_IN_MANIFEST]` |
| `214` | `Mod_StArena_Base` | `18` | `open_st_arena, refresh_player_list` | `[READY_IN_MANIFEST]` |
| `215` | `Mod_Archery_Base` | `7` | `act_open_time, act_info` | `[READY_IN_MANIFEST]` |
| `216` | `Mod_CourtyardPet_Base` | `17` | `get_player_info, call` | `[READY_IN_MANIFEST]` |
| `217` | `Mod_Fish_Base` | `2` | `get_player_fishhook, do_fishing` | `[READY_IN_MANIFEST]` |
| `218` | `Mod_SpringActivity_Base` | `33` | `get_activity_info, notify` | `[READY_IN_MANIFEST]` |
| `219` | `Mod_CourtyardFurnance_Base` | `15` | `smelt, get_resource_list` | `[READY_IN_MANIFEST]` |
| `220` | `Mod_FairyGourd_Base` | `3` | `get_date, get_fairy_gourd_list` | `[READY_IN_MANIFEST]` |
| `221` | `Mod_NewServerFund_Base` | `4` | `is_can_buy_new_server_fund, new_server_fund_info` | `[READY_IN_MANIFEST]` |
| `222` | `Mod_FoolsDay_Base` | `2` | `fools_day_info, dig` | `[READY_IN_MANIFEST]` |
| `223` | `Mod_StUnionBesiege_Base` | `26` | `get_activity_state, notify` | `[READY_IN_MANIFEST]` |
| `224` | `Mod_StUnionBesiegeHonorShop_Base` | `2` | `buy, get_bought_list` | `[READY_IN_MANIFEST]` |
| `225` | `Mod_Memoirs_Base` | `43` | `is_open_new, get_player_memoirs` | `[READY_IN_MANIFEST]` |
| `226` | `Mod_SuitEquip_Base` | `8` | `get_info, buy_suit` | `[READY_IN_MANIFEST]` |
| `227` | `Mod_NewServerDaren_Base` | `3` | `new_server_daren_info, receive_quest_award` | `[READY_IN_MANIFEST]` |
| `228` | `Mod_LostDeploy_Base` | `4` | `get_player_lost_deploy_info, activate_artifact` | `[READY_IN_MANIFEST]` |
| `229` | `Mod_ActiveDig_Base` | `2` | `active_dig_info, dig` | `[READY_IN_MANIFEST]` |
| `230` | `Mod_NewWorldPk_Base` | `27` | `get_my_room_info, get_room_list` | `[READY_IN_MANIFEST]` |
| `231` | `Mod_FourthAnniversaryFightCard_Base` | `4` | `get_info, fight` | `[READY_IN_MANIFEST]` |
| `232` | `Mod_LinkFate_Base` | `25` | `get_link_fate_info, equip_link_fate_stone` | `[READY_IN_MANIFEST]` |
| `233` | `Mod_LinkFatePve_Base` | `2` | `get_info, fight` | `[READY_IN_MANIFEST]` |
| `234` | `Mod_StUnionGuardWar_Base` | `18` | `get_info, get_st_unions` | `[READY_IN_MANIFEST]` |
| `235` | `Mod_PotWorld_Base` | `17` | `get_info, get_store_info` | `[READY_IN_MANIFEST]` |
| `236` | `Mod_StIndianaJones_Base` | `25` | `get_activity_indiana_jones_info, get_player_indiana_jones_info` | `[READY_IN_MANIFEST]` |
| `237` | `Mod_StJinBangTiMing_Base` | `7` | `get_activity_time_status_info, get_player_jin_bang_info` | `[READY_IN_MANIFEST]` |
| `238` | `Mod_PowerFame_Base` | `3` | `get_player_power_fame_info, activate_power_fame_supernatural` | `[READY_IN_MANIFEST]` |
| `239` | `Mod_MagicTreasure_Base` | `6` | `get_info, draw` | `[READY_IN_MANIFEST]` |
| `240` | `Mod_ReleaseWelfare_Base` | `5` | `get_info, get_welfare` | `[READY_IN_MANIFEST]` |
| `241` | `Mod_FanFanLe_Base` | `3` | `get_info, flop` | `[READY_IN_MANIFEST]` |
| `242` | `Mod_SundayFruit_Base` | `3` | `active_status, sunday_fruit_info` | `[READY_IN_MANIFEST]` |
| `243` | `Mod_TianShu_Base` | `12` | `get_info, active` | `[READY_IN_MANIFEST]` |
| `244` | `Mod_GuanXing_Base` | `4` | `get_info, explore` | `[READY_IN_MANIFEST]` |
| `245` | `Mod_StPiebridge_Base` | `15` | `get_player_info, notify` | `[READY_IN_MANIFEST]` |
| `246` | `Mod_MagpieActivityLuckyWheel_Base` | `4` | `lucky_wheel_info, lottery` | `[READY_IN_MANIFEST]` |
| `247` | `Mod_Juyuan_Base` | `13` | `get_info, merge_spirit` | `[READY_IN_MANIFEST]` |
| `248` | `Mod_DayFallsGift_Base` | `3` | `day_falls_info, get_gift` | `[READY_IN_MANIFEST]` |
| `249` | `Mod_FindKey_Base` | `6` | `find_key_info, buy_find_times` | `[READY_IN_MANIFEST]` |
| `250` | `Mod_StPanTao_Base` | `19` | `get_activity_step, notify_step` | `[READY_IN_MANIFEST]` |
| `251` | `Mod_MiracleFighters_Base` | `7` | `get_miracle_fighters_info, practice_miracle_fighters` | `[READY_IN_MANIFEST]` |
| `252` | `Mod_ZodiacDivination_Base` | `5` | `get_zodiac_divination_info, divination` | `[READY_IN_MANIFEST]` |
| `253` | `Mod_MiracleFightersPve_Base` | `2` | `get_player_info, fight` | `[READY_IN_MANIFEST]` |
| `254` | `Mod_Regression_Base` | `7` | `get_player_regression_login_info, dice` | `[READY_IN_MANIFEST]` |
| `255` | `Mod_StUndergroundPalace_Base` | `14` | `get_activity_info, get_player_st_underground_palace_info` | `[READY_IN_MANIFEST]` |
| `256` | `Mod_Jindouyun_Base` | `5` | `enter_race, turbo` | `[READY_IN_MANIFEST]` |
| `257` | `Mod_StUnionSixvsix_Base` | `32` | `get_my_team, get_team_list` | `[READY_IN_MANIFEST]` |
| `258` | `Mod_StUnionSixvsixShop_Base` | `2` | `get_exchange_list, exchange` | `[READY_IN_MANIFEST]` |
| `259` | `Mod_LunHui_Base` | `21` | `get_info, merge_stone` | `[READY_IN_MANIFEST]` |
| `260` | `Mod_WagerShop_Base` | `24` | `get_twenty_one_info, bet_twenty_one` | `[READY_IN_MANIFEST]` |
| `261` | `Mod_GhostlyTower_Base` | `7` | `get_info, get_deploy` | `[READY_IN_MANIFEST]` |
| `262` | `Mod_MainRoleSaint_Base` | `3` | `get_info, saint` | `[READY_IN_MANIFEST]` |
| `263` | `Mod_StAltar_Base` | `9` | `get_altar_info, get_quest_list` | `[READY_IN_MANIFEST]` |
| `264` | `Mod_StMine_Base` | `35` | `get_mine_mountain_info, enter_mine_mountain` | `[READY_IN_MANIFEST]` |
| `265` | `Mod_MountUpgrade_Base` | `8` | `get_info, active_rune_point` | `[READY_IN_MANIFEST]` |
| `266` | `Mod_FestivalMessenger_Base` | `4` | `get_info, get_award` | `[READY_IN_MANIFEST]` |
| `267` | `Mod_DoubleTurntable_Base` | `10` | `get_turntable_info, turntable` | `[READY_IN_MANIFEST]` |
| `268` | `Mod_LuckyBag_Base` | `2` | `get_info, get_bag` | `[READY_IN_MANIFEST]` |
| `269` | `Mod_CardSoulMachine_Base` | `4` | `get_machine_info, start` | `[READY_IN_MANIFEST]` |
| `270` | `Mod_SageQuicken_Base` | `2` | `get_info, buy_item` | `[READY_IN_MANIFEST]` |
| `271` | `Mod_FindSingleDog_Base` | `7` | `get_info, start_find` | `[READY_IN_MANIFEST]` |
| `272` | `Mod_BaiLianQianKun_Base` | `9` | `get_info, challenge` | `[READY_IN_MANIFEST]` |
| `273` | `Mod_MagicWeapon_Base` | `28` | `get_magic_weapon_info, get_magic_weapon_picture` | `[READY_IN_MANIFEST]` |
| `274` | `Mod_ConsumeTalent_Base` | `3` | `get_activity_info, open_panel` | `[READY_IN_MANIFEST]` |
| `275` | `Mod_SpecialEffect_Base` | `5` | `get_info, upgrade` | `[READY_IN_MANIFEST]` |
| `276` | `Mod_QingmingBurning_Base` | `2` | `get_info, burning` | `[READY_IN_MANIFEST]` |
| `277` | `Mod_LiangYiBaGua_Base` | `5` | `get_info, open_panel` | `[READY_IN_MANIFEST]` |
| `278` | `Mod_WishWall_Base` | `4` | `get_wish_wall_info, wish` | `[READY_IN_MANIFEST]` |
| `279` | `Mod_StSharptimeGift_Base` | `5` | `get_info, get_award` | `[READY_IN_MANIFEST]` |
| `280` | `Mod_SantWeapon_Base` | `13` | `get_sant_weapon_info, make_sant_weapon` | `[READY_IN_MANIFEST]` |
| `281` | `Mod_ClearLine_Base` | `3` | `result_score, get_exchange_list` | `[READY_IN_MANIFEST]` |
| `282` | `Mod_RefinePool_Base` | `4` | `open_panel, refine` | `[READY_IN_MANIFEST]` |
| `283` | `Mod_TwoCardMeet_Base` | `5` | `get_info, start` | `[READY_IN_MANIFEST]` |
| `284` | `Mod_StNationalRedBag_Base` | `7` | `get_info, snatch` | `[READY_IN_MANIFEST]` |
| `285` | `Mod_StFunCityOpen_Base` | `14` | `open_panel, start_answer` | `[READY_IN_MANIFEST]` |
| `286` | `Mod_StBigTurntable_Base` | `2` | `get_big_turntable_info, turntable` | `[READY_IN_MANIFEST]` |
| `287` | `Mod_HideTreasureMap_Base` | `6` | `player_use_grid_item, start_grub` | `[READY_IN_MANIFEST]` |
| `288` | `Mod_FunCityMedal_Base` | `2` | `get_medal_info, get_medal` | `[READY_IN_MANIFEST]` |
| `289` | `Mod_StPetAllStar_Base` | `14` | `get_pet_all_star_status, pve_quest_info` | `[READY_IN_MANIFEST]` |
| `290` | `Mod_PartnerLink_Base` | `11` | `get_info, activate` | `[READY_IN_MANIFEST]` |
| `291` | `Mod_SaPractice_Base` | `6` | `get_enter_saint_area_info, find` | `[READY_IN_MANIFEST]` |
| `292` | `Mod_StSixOneShopping_Base` | `7` | `get_info, bug_item` | `[READY_IN_MANIFEST]` |
| `293` | `Mod_SaintAreaLogin_Base` | `5` | `login, get_login_info` | `[READY_IN_MANIFEST]` |
| `294` | `Mod_SaintAreaTown_Base` | `11` | `enter_town, notify_enter_town` | `[READY_IN_MANIFEST]` |
| `295` | `Mod_SaPk_Base` | `8` | `direct_pk, invite_pk` | `[READY_IN_MANIFEST]` |
| `296` | `Mod_FriendPractice_Base` | `7` | `get_info, invite_friend` | `[READY_IN_MANIFEST]` |
| `297` | `Mod_StTwinDragons_Base` | `37` | `get_player_twin_dragons_team, get_all_twin_dragons_team` | `[READY_IN_MANIFEST]` |
| `298` | `Mod_SaArena_Base` | `11` | `get_info, rob_the_seat` | `[READY_IN_MANIFEST]` |
| `299` | `Mod_Tactics_Base` | `12` | `get_tactics_info, draw_tactics_exp` | `[READY_IN_MANIFEST]` |
| `300` | `Mod_BallFight_Base` | `4` | `open_panel, ball_fight_game_over` | `[READY_IN_MANIFEST]` |
| `301` | `Mod_RechargeOpenBox_Base` | `6` | `get_info, open_panel` | `[READY_IN_MANIFEST]` |
| `302` | `Mod_LanternsLottery_Base` | `7` | `get_lanterns_lottery_info, start_lottery` | `[READY_IN_MANIFEST]` |
| `303` | `Mod_AchievementPartner_Base` | `9` | `achievement_partner_info, upgrade` | `[READY_IN_MANIFEST]` |
| `304` | `Mod_Vote_Base` | `6` | `get_vote_info, vote` | `[READY_IN_MANIFEST]` |
| `305` | `Mod_StTreasureFight_Base` | `21` | `get_activity_state, notify_state_change` | `[READY_IN_MANIFEST]` |
| `306` | `Mod_PartnerPractice_Base` | `13` | `get_partner_practice_info, select_partner` | `[READY_IN_MANIFEST]` |
| `307` | `Mod_StVoice_Base` | `9` | `get_race_step, update_step` | `[READY_IN_MANIFEST]` |
| `308` | `Mod_JobChange_Base` | `2` | `get_job_change_info, change` | `[READY_IN_MANIFEST]` |
| `309` | `Mod_AttributeStone_Base` | `9` | `role_info_list, attribute_stone_list` | `[READY_IN_MANIFEST]` |
| `310` | `Mod_RopeGame_Base` | `2` | `get_rope_game_info, game_over` | `[READY_IN_MANIFEST]` |
| `311` | `Mod_StLuckySuperNumber_Base` | `3` | `get_lucky_super_number_info, draw` | `[READY_IN_MANIFEST]` |
| `312` | `Mod_Children_Base` | `54` | `get_info, rename` | `[READY_IN_MANIFEST]` |
| `313` | `Mod_ChildrenSearch_Base` | `5` | `get_search_info, get_deploy` | `[READY_IN_MANIFEST]` |
| `314` | `Mod_RobMoney_Base` | `14` | `get_rob_money_info, search` | `[READY_IN_MANIFEST]` |
| `315` | `Mod_ChildrenTask_Base` | `4` | `get_children_task_info, get_award` | `[READY_IN_MANIFEST]` |
| `316` | `Mod_NumberTreasure_Base` | `2` | `get_number_treasure_info, draw` | `[READY_IN_MANIFEST]` |
| `317` | `Mod_NewShuiYuZhengFeng_Base` | `27` | `sign_up, get_player_shui_lu` | `[READY_IN_MANIFEST]` |
| `318` | `Mod_AddupRechargeActivity_Base` | `5` | `get_activity_state, get_player_addup_recharge_info` | `[READY_IN_MANIFEST]` |
| `319` | `Mod_SmallScoreGame_Base` | `2` | `open_panel, game_over` | `[READY_IN_MANIFEST]` |
| `320` | `Mod_BaiLianQianKunTwo_Base` | `9` | `get_info, challenge` | `[READY_IN_MANIFEST]` |
| `321` | `Mod_StMarriageTape_Base` | `5` | `get_tape_info, get_wall_info` | `[READY_IN_MANIFEST]` |
| `322` | `Mod_PartnerSoul_Base` | `20` | `get_fight_turntable_info, unlock` | `[READY_IN_MANIFEST]` |
| `323` | `Mod_FuShiHall_Base` | `6` | `get_hall_info, bless` | `[READY_IN_MANIFEST]` |
| `324` | `Mod_RuneStoneMission_Base` | `3` | `get_info, enter_mission` | `[READY_IN_MANIFEST]` |
| `325` | `Mod_WishingWell_Base` | `4` | `get_info, wishing` | `[READY_IN_MANIFEST]` |
| `326` | `Mod_NewServerVariesFunds_Base` | `5` | `is_open, activity_info` | `[READY_IN_MANIFEST]` |
| `327` | `Mod_SaintSpeedMonth_Base` | `4` | `get_saint_speed_month_info, get_award` | `[READY_IN_MANIFEST]` |
| `328` | `Mod_GodWelfare_Base` | `3` | `get_god_welfare_info, get_level_award_info` | `[READY_IN_MANIFEST]` |
| `329` | `Mod_StHirePartner_Base` | `11` | `get_info, open_panel` | `[READY_IN_MANIFEST]` |
| `330` | `Mod_NewYearCumulativeLogin_Base` | `2` | `get_info, get_award` | `[READY_IN_MANIFEST]` |
| `331` | `Mod_ChristmasGift_Base` | `5` | `get_sock_info, get_sock` | `[READY_IN_MANIFEST]` |
| `332` | `Mod_Pawnshop_Base` | `12` | `get_info, pawn` | `[READY_IN_MANIFEST]` |
| `333` | `Mod_LimitShop_Base` | `4` | `get_limit_shop_info, buy_good` | `[READY_IN_MANIFEST]` |
| `334` | `Mod_StFlyEgg_Base` | `6` | `get_fly_egg_activity_info, notify_fly_egg_activity_status_change` | `[READY_IN_MANIFEST]` |
| `335` | `Mod_ClientFlag_Base` | `2` | `get_all_flag, get_single_mod_flag` | `[READY_IN_MANIFEST]` |
| `336` | `Mod_ServerChatRoom_Base` | `58` | `get_recent_room_list, get_chat_room_status` | `[READY_IN_MANIFEST]` |
| `337` | `Mod_StUnionTask_Base` | `4` | `get_challenge_info, fight` | `[READY_IN_MANIFEST]` |
| `338` | `Mod_HorseSkill_Base` | `19` | `player_role_list, equip_horse_stone` | `[READY_IN_MANIFEST]` |
| `339` | `Mod_SpringFestivalChicken_Base` | `14` | `get_red_bag_rain_info, red_bag_rain_notify` | `[READY_IN_MANIFEST]` |
| `340` | `Mod_NewYearSmallActivity_Base` | `4` | `get_player_ying_fu_login_state, get_ying_fu_award` | `[READY_IN_MANIFEST]` |
| `341` | `Mod_ServerTower_Base` | `25` | `get_open_flag, open_panel` | `[READY_IN_MANIFEST]` |
| `342` | `Mod_SuperTownUpdateFeedback_Base` | `1` | `get_feedback_info` | `[READY_IN_MANIFEST]` |
| `343` | `Mod_ChildrenPracticeProperty_Base` | `3` | `get_children_practice_property_info, refining` | `[READY_IN_MANIFEST]` |
| `344` | `Mod_DanceAction_Base` | `3` | `get_dance_action_info, use_action` | `[READY_IN_MANIFEST]` |
| `345` | `Mod_Email_Base` | `7` | `get_email_info, read_email` | `[READY_IN_MANIFEST]` |
| `346` | `Mod_SpringOuting_Base` | `7` | `open_peal, chooid_spring_outing` | `[READY_IN_MANIFEST]` |
| `347` | `Mod_ElixirSoul_Base` | `7` | `get_role_info, activate_elixir_soul` | `[READY_IN_MANIFEST]` |
| `348` | `Mod_MoonlightBox_Base` | `7` | `get_moonlight_box_info, rock` | `[READY_IN_MANIFEST]` |
| `349` | `Mod_WorldPkRanking_Base` | `34` | `get_status, notify_status_change` | `[READY_IN_MANIFEST]` |
| `350` | `Mod_SixthAnniversaryCake_Base` | `2` | `get_sixth_anniversary_cake_info, eat_cake` | `[READY_IN_MANIFEST]` |
| `351` | `Mod_SixthAnniversaryTreasure_Base` | `3` | `get_sixth_anniversary_treasure_info, meet` | `[READY_IN_MANIFEST]` |
| `352` | `Mod_BraveRoad_Base` | `3` | `get_brave_road_info, get_award` | `[READY_IN_MANIFEST]` |
| `353` | `Mod_LuckyStarEvent_Base` | `3` | `get_day_info, get_award` | `[READY_IN_MANIFEST]` |
| `354` | `Mod_FairyBag_Base` | `2` | `get_fairy_bag_info, get_coins` | `[READY_IN_MANIFEST]` |
| `355` | `Mod_RunOfLuck_Base` | `4` | `get_run_of_luck_info, start` | `[READY_IN_MANIFEST]` |
| `356` | `Mod_DunhuangTreasure_Base` | `5` | `get_dunhuang_treasure_info, open_treasure` | `[READY_IN_MANIFEST]` |
| `357` | `Mod_Levitate_Base` | `6` | `get_levitate_info, perfusion` | `[READY_IN_MANIFEST]` |
| `358` | `Mod_ChildrenDayBox_Base` | `5` | `get_info, refresh` | `[READY_IN_MANIFEST]` |
| `359` | `Mod_WishPool_Base` | `7` | `get_wish_pool_info, get_wish_list` | `[READY_IN_MANIFEST]` |
| `360` | `Mod_DayFunds_Base` | `5` | `is_can_buy_day_funds, get_day_funds_info` | `[READY_IN_MANIFEST]` |
| `361` | `Mod_SummerScratch_Base` | `5` | `scratch_info, get_card` | `[READY_IN_MANIFEST]` |
| `362` | `Mod_SaDragonArea_Base` | `5` | `get_dragon_area_info, get_top_10` | `[READY_IN_MANIFEST]` |
| `363` | `Mod_StDrawingGuess_Base` | `18` | `get_drawing_guess_info, begin_match` | `[READY_IN_MANIFEST]` |
| `364` | `Mod_RewardTask_Base` | `5` | `get_reward_task_info, accept` | `[READY_IN_MANIFEST]` |
| `365` | `Mod_ChildrenSuit_Base` | `4` | `get_children_suit_info, use_suit` | `[READY_IN_MANIFEST]` |
| `366` | `Mod_LevitateMaterial_Base` | `3` | `get_levitate_material_info, buy` | `[READY_IN_MANIFEST]` |
| `367` | `Mod_GoldTower_Base` | `13` | `tower_info, draw` | `[READY_IN_MANIFEST]` |
| `368` | `Mod_JobStrengthen_Base` | `4` | `get_prop_num, get_rune_list` | `[READY_IN_MANIFEST]` |
| `369` | `Mod_GuessPartner_Base` | `4` | `guess_partner_info, start_guess` | `[READY_IN_MANIFEST]` |
| `370` | `Mod_StMatchesWarPrepare_Base` | `7` | `get_competitor_info, apply` | `[READY_IN_MANIFEST]` |
| `371` | `Mod_StMatchesCup_Base` | `23` | `get_cup_info, serialize_war_report` | `[READY_IN_MANIFEST]` |
| `372` | `Mod_StBridgeBless_Base` | `8` | `st_bridge_bless_info, get_prop` | `[READY_IN_MANIFEST]` |
| `373` | `Mod_Sanyo_Base` | `3` | `get_sanyo_info, buy_goods` | `[READY_IN_MANIFEST]` |
| `374` | `Mod_CoinMission_Base` | `6` | `get_coin_mission_info, fight` | `[READY_IN_MANIFEST]` |
| `375` | `Mod_StWishBag_Base` | `7` | `get_wish_bag_info, make` | `[READY_IN_MANIFEST]` |
| `376` | `Mod_NationalDayShop_Base` | `4` | `shop_info, buy_goods` | `[READY_IN_MANIFEST]` |
| `377` | `Mod_MidautuGame_Base` | `3` | `get_midautu_game_info, get_player_rank` | `[READY_IN_MANIFEST]` |
| `378` | `Mod_MidBackLottery_Base` | `4` | `get_back_lottery_info, back_lottery` | `[READY_IN_MANIFEST]` |
| `379` | `Mod_FiveDeploy_Base` | `8` | `five_deploy_info, get_deploy` | `[READY_IN_MANIFEST]` |
| `380` | `Mod_Artifact_Base` | `10` | `get_artifact_info, unlock_skill` | `[READY_IN_MANIFEST]` |
| `381` | `Mod_OneOneSales_Base` | `2` | `get_sales_info, buy` | `[READY_IN_MANIFEST]` |
| `382` | `Mod_HalloweenActivity_Base` | `4` | `get_question_and_answer, submit_question_and_answer` | `[READY_IN_MANIFEST]` |
| `383` | `Mod_NineDoor_Base` | `8` | `get_nine_door_info, open_door` | `[READY_IN_MANIFEST]` |
| `384` | `Mod_SaSuperSport_Base` | `9` | `race_info, rank_list` | `[READY_IN_MANIFEST]` |
| `385` | `Mod_NanTianGate_Base` | `6` | `get_nan_tian_gate_info, get_deploy` | `[READY_IN_MANIFEST]` |
| `386` | `Mod_StUnionAnimal_Base` | `5` | `get_animal_info, get_ranking_info` | `[READY_IN_MANIFEST]` |
| `387` | `Mod_DoubleGoodThings_Base` | `5` | `get_double_good_things_info, lottery_draw` | `[READY_IN_MANIFEST]` |
| `388` | `Mod_WinterJiaozi_Base` | `3` | `activity_info, eat_dumplings` | `[READY_IN_MANIFEST]` |
| `389` | `Mod_DragonChallenge_Base` | `4` | `get_dragon_challenge_info, buy_times` | `[READY_IN_MANIFEST]` |
| `390` | `Mod_ChiJiInChristmas_Base` | `3` | `activity_info, chi_ji` | `[READY_IN_MANIFEST]` |
| `391` | `Mod_WealthGodBefall_Base` | `3` | `activity_info, open_box` | `[READY_IN_MANIFEST]` |
| `392` | `Mod_MiracleFightersTwo_Base` | `7` | `get_miracle_fighters_info, practice_miracle_fighters` | `[READY_IN_MANIFEST]` |
| `393` | `Mod_IceCaveTreasure_Base` | `4` | `activity_info, hit_ice` | `[READY_IN_MANIFEST]` |
| `394` | `Mod_MiracleFightersPveTwo_Base` | `2` | `get_player_info, fight` | `[READY_IN_MANIFEST]` |
| `395` | `Mod_SaTakeBible_Base` | `26` | `open_take_bible, close_take_bible` | `[READY_IN_MANIFEST]` |
| `396` | `Mod_JumpOneJump_Base` | `5` | `activity_info, round_over` | `[READY_IN_MANIFEST]` |
| `397` | `Mod_StFriend_Base` | `20` | `add_friend, add_to_black` | `[READY_IN_MANIFEST]` |
| `398` | `Mod_SaFriend_Base` | `20` | `add_friend, add_to_black` | `[READY_IN_MANIFEST]` |
| `399` | `Mod_MakeWine_Base` | `9` | `get_info, wine_make` | `[READY_IN_MANIFEST]` |
| `400` | `Mod_FiveFu_Base` | `7` | `get_info, open_pack` | `[READY_IN_MANIFEST]` |
| `401` | `Mod_FunctionHerald_Base` | `4` | `get_function_herald_panel_status, get_function_herald_info` | `[READY_IN_MANIFEST]` |
| `402` | `Mod_PartnerVote_Base` | `7` | `get_race_step, apply_info` | `[READY_IN_MANIFEST]` |
| `403` | `Mod_FaXiang_Base` | `6` | `get_fa_xiang_info, lighten_fo` | `[READY_IN_MANIFEST]` |
| `404` | `Mod_MakeGoodStart_Base` | `6` | `get_info, write_num` | `[READY_IN_MANIFEST]` |
| `405` | `Mod_LuckyPoker_Base` | `4` | `get_info, lottery_draw` | `[READY_IN_MANIFEST]` |
| `406` | `Mod_FoolsDayAdventure_Base` | `5` | `open_panel, start_adventure` | `[READY_IN_MANIFEST]` |
| `407` | `Mod_SaPracticeRoom_Base` | `19` | `get_rooms, get_room_info` | `[READY_IN_MANIFEST]` |
| `408` | `Mod_QingMingBless_Base` | `6` | `get_info, bless` | `[READY_IN_MANIFEST]` |
| `409` | `Mod_WeekendPractice_Base` | `10` | `get_state, open_panel` | `[READY_IN_MANIFEST]` |
| `410` | `Mod_ModelWorker_Base` | `5` | `get_info, player_recommend` | `[READY_IN_MANIFEST]` |
| `411` | `Mod_DemonInvasion_Base` | `8` | `get_state, open_panel` | `[READY_IN_MANIFEST]` |
| `412` | `Mod_TianDaoChouQin_Base` | `4` | `get_info, free_get` | `[READY_IN_MANIFEST]` |
| `413` | `Mod_SaUnion_Base` | `28` | `get_sa_union_list, get_request_sa_union_list` | `[READY_IN_MANIFEST]` |
| `414` | `Mod_LotteryInMagicBox_Base` | `8` | `get_info, combination` | `[READY_IN_MANIFEST]` |
| `415` | `Mod_AllPeopleFeed_Base` | `6` | `get_seven_year_exchange_info, seven_year_exchange` | `[READY_IN_MANIFEST]` |
| `416` | `Mod_SaUnionBless_Base` | `2` | `sa_union_bless_info, bless` | `[READY_IN_MANIFEST]` |
| `417` | `Mod_DiceMessenger_Base` | `4` | `get_info, play_dice` | `[READY_IN_MANIFEST]` |
| `418` | `Mod_OriginTrial_Base` | `4` | `get_info, fight` | `[READY_IN_MANIFEST]` |
| `419` | `Mod_SaUnionWorship_Base` | `5` | `open_panel, worship` | `[READY_IN_MANIFEST]` |
| `420` | `Mod_AnniversaryLuckBag_Base` | `4` | `get_info, produce_bag` | `[READY_IN_MANIFEST]` |
| `421` | `Mod_MemoryReel_Base` | `4` | `get_info, clean_photo` | `[READY_IN_MANIFEST]` |
| `422` | `Mod_FeedbackBox_Base` | `3` | `get_info, buy_box` | `[READY_IN_MANIFEST]` |
| `423` | `Mod_SaUnionWar_Base` | `17` | `notify_status, get_player_sa_union_war_status` | `[READY_IN_MANIFEST]` |
| `424` | `Mod_HeadPortrait_Base` | `4` | `head_portrait_list, set_head_portrait` | `[READY_IN_MANIFEST]` |
| `425` | `Mod_GoBackTask_Base` | `3` | `get_info, get_award` | `[READY_IN_MANIFEST]` |
| `426` | `Mod_GoBackPrivilege_Base` | `1` | `go_back_privilege_info` | `[READY_IN_MANIFEST]` |
| `427` | `Mod_CoolSummer_Base` | `3` | `open_panel, get_today_award` | `[READY_IN_MANIFEST]` |
| `428` | `Mod_PassionSummerLottery_Base` | `4` | `get_info, get_award_info` | `[READY_IN_MANIFEST]` |
| `429` | `Mod_DevilExpedition_Base` | `77` | `activity_status, open_match_panel` | `[READY_IN_MANIFEST]` |
| `430` | `Mod_ExpeditionTask_Base` | `2` | `get_info, start_task` | `[READY_IN_MANIFEST]` |
| `431` | `Mod_SuperValueBag_Base` | `3` | `get_info, buy_gift` | `[READY_IN_MANIFEST]` |
| `432` | `Mod_NewServiceCoupons_Base` | `7` | `get_info, lottery` | `[READY_IN_MANIFEST]` |
| `433` | `Mod_RechargeFund_Base` | `3` | `get_info, activation` | `[READY_IN_MANIFEST]` |
| `434` | `Mod_MagpieFestivalCollect_Base` | `6` | `get_info, exchange_gift` | `[READY_IN_MANIFEST]` |
| `435` | `Mod_StGuessNumber_Base` | `12` | `get_activity_status, open_activity_panel` | `[READY_IN_MANIFEST]` |
| `436` | `Mod_NpcFriendship_Base` | `12` | `get_info, get_give_present_info` | `[READY_IN_MANIFEST]` |
| `437` | `Mod_SaRanking_Base` | `3` | `sa_ranking_list, get_ranking_info` | `[READY_IN_MANIFEST]` |
| `438` | `Mod_SummerTreasureBox_Base` | `5` | `open_panel, unlock_box` | `[READY_IN_MANIFEST]` |
| `439` | `Mod_MidAutumnGift_Base` | `3` | `get_info, gain_award` | `[READY_IN_MANIFEST]` |
| `440` | `Mod_WorldFriend_Base` | `14` | `send_add_friend, accept_add_friend` | `[READY_IN_MANIFEST]` |
| `441` | `Mod_FullMoonMidAutumn_Base` | `6` | `get_info, get_player_cake_info` | `[READY_IN_MANIFEST]` |
| `442` | `Mod_NationalDayWish_Base` | `5` | `open_panel, open_select` | `[READY_IN_MANIFEST]` |
| `443` | `Mod_SaUnionTower_Base` | `9` | `get_info, get_fight_panel_info` | `[READY_IN_MANIFEST]` |
| `444` | `Mod_BestLineupChallenge_Base` | `31` | `get_info, get_main_role_panel_info` | `[READY_IN_MANIFEST]` |
| `445` | `Mod_DoubleElevenGift_Base` | `7` | `double_eleven_gift_info, open_gift` | `[READY_IN_MANIFEST]` |
| `446` | `Mod_FirstRecharge_Base` | `2` | `get_panel_info, gain_gift` | `[READY_IN_MANIFEST]` |
| `447` | `Mod_NewServerRank_Base` | `4` | `new_server_rank_open_time, new_server_rank_info` | `[READY_IN_MANIFEST]` |
| `448` | `Mod_NewServerLuckyTree_Base` | `4` | `get_status, open_panel` | `[READY_IN_MANIFEST]` |
| `449` | `Mod_MonsterGodPalace_Base` | `12` | `get_panel_info, call_monster_god` | `[READY_IN_MANIFEST]` |
| `450` | `Mod_ChristmasSendGift_Base` | `4` | `get_panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `451` | `Mod_NewYearGoldEgg_Base` | `5` | `get_panel_info, hit_egg` | `[READY_IN_MANIFEST]` |
| `452` | `Mod_NewYearBadges_Base` | `3` | `new_year_badges_info, alight` | `[READY_IN_MANIFEST]` |
| `453` | `Mod_FiveElementsPalace_Base` | `11` | `five_elements_info, get_deploy` | `[READY_IN_MANIFEST]` |
| `454` | `Mod_NewYearNpcBainian_Base` | `5` | `open_panel, get_award` | `[READY_IN_MANIFEST]` |
| `455` | `Mod_NewYearGoldPig_Base` | `4` | `panel_info, put_in_money` | `[READY_IN_MANIFEST]` |
| `456` | `Mod_MainRoleRebirth_Base` | `9` | `open_panel, get_deploy` | `[READY_IN_MANIFEST]` |
| `457` | `Mod_SpringBigRun_Base` | `3` | `panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `458` | `Mod_NewYearFund_Base` | `6` | `new_year_fund_info, buy_new_year_fund` | `[READY_IN_MANIFEST]` |
| `459` | `Mod_GoBackShop_Base` | `2` | `open_panel, buy_shop_item` | `[READY_IN_MANIFEST]` |
| `460` | `Mod_FateStarPlate_Base` | `4` | `panel_info, light_star` | `[READY_IN_MANIFEST]` |
| `461` | `Mod_GoBackLogin_Base` | `2` | `open_panel, get_award` | `[READY_IN_MANIFEST]` |
| `462` | `Mod_PartnerExpedition_Base` | `5` | `panel_info, go_on` | `[READY_IN_MANIFEST]` |
| `463` | `Mod_XingXiu_Base` | `6` | `open_panel, light_point` | `[READY_IN_MANIFEST]` |
| `464` | `Mod_ThanksFeedback_Base` | `2` | `open_panel, get_award` | `[READY_IN_MANIFEST]` |
| `465` | `Mod_TurntableDraw_Base` | `4` | `panel_info, ingot_draw` | `[READY_IN_MANIFEST]` |
| `466` | `Mod_SeekImmortalRoad_Base` | `16` | `open_panel, buy_advanced` | `[READY_IN_MANIFEST]` |
| `467` | `Mod_StShanhaiRelic_Base` | `33` | `activity_state, prepare_panel` | `[READY_IN_MANIFEST]` |
| `468` | `Mod_MayDayFindTreasure_Base` | `4` | `may_day_find_treasure_info, buy_hammer` | `[READY_IN_MANIFEST]` |
| `469` | `Mod_Furinkazan_Base` | `9` | `panel_info, deploy_info` | `[READY_IN_MANIFEST]` |
| `470` | `Mod_EightYearMedal_Base` | `2` | `eight_year_medal_info, get_medal_award` | `[READY_IN_MANIFEST]` |
| `471` | `Mod_FourZoneRank_Base` | `1` | `rank_list` | `[READY_IN_MANIFEST]` |
| `472` | `Mod_MammonBless_Base` | `1` | `get_info` | `[READY_IN_MANIFEST]` |
| `473` | `Mod_ThearchyBiography_Base` | `9` | `panel_info, train_info` | `[READY_IN_MANIFEST]` |
| `474` | `Mod_EightYearMine_Base` | `2` | `panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `475` | `Mod_Pinnacle_Base` | `2` | `pinnacle_info, set_hid` | `[READY_IN_MANIFEST]` |
| `476` | `Mod_SkyMelee_Base` | `12` | `open_panel, select_diff` | `[READY_IN_MANIFEST]` |
| `477` | `Mod_RefineTreasure_Base` | `17` | `panel_info, create_team` | `[READY_IN_MANIFEST]` |
| `478` | `Mod_NewServerLogin_Base` | `4` | `get_state, open_panel` | `[READY_IN_MANIFEST]` |
| `479` | `Mod_HeavenHero_Base` | `10` | `panel_info, deploy_info` | `[READY_IN_MANIFEST]` |
| `480` | `Mod_MazeTreasure_Base` | `6` | `open_panel, challenge` | `[READY_IN_MANIFEST]` |
| `481` | `Mod_SummerFindTreasure_Base` | `4` | `open_panel, use_bomb` | `[READY_IN_MANIFEST]` |
| `482` | `Mod_QijueArray_Base` | `8` | `open_panel, get_deploy` | `[READY_IN_MANIFEST]` |
| `483` | `Mod_YuanShengWorld_Base` | `14` | `get_info, complete_quest` | `[READY_IN_MANIFEST]` |
| `484` | `Mod_QiXiExchange_Base` | `6` | `qi_xi_exchange_info, get_item` | `[READY_IN_MANIFEST]` |
| `485` | `Mod_StarPicture_Base` | `9` | `get_info, divination` | `[READY_IN_MANIFEST]` |
| `486` | `Mod_MagicArray_Base` | `15` | `open_panel, partner_list` | `[READY_IN_MANIFEST]` |
| `487` | `Mod_SaBattle_Base` | `14` | `activity_status, entry_panel` | `[READY_IN_MANIFEST]` |
| `488` | `Mod_SchoolOpenShop_Base` | `7` | `get_info, buy_item` | `[READY_IN_MANIFEST]` |
| `489` | `Mod_GoBackScore_Base` | `4` | `go_back_active_info, go_back_score_info` | `[READY_IN_MANIFEST]` |
| `490` | `Mod_SchoolOpenRecall_Base` | `6` | `get_info, be_invite` | `[READY_IN_MANIFEST]` |
| `491` | `Mod_NewServerRecommend_Base` | `5` | `get_info, gain_award` | `[READY_IN_MANIFEST]` |
| `492` | `Mod_PraySigning_Base` | `10` | `get_info, pray` | `[READY_IN_MANIFEST]` |
| `493` | `Mod_FortuneStick_Base` | `4` | `open_panel, lottery` | `[READY_IN_MANIFEST]` |
| `494` | `Mod_NewChargeBack_Base` | `5` | `get_info, get_award` | `[READY_IN_MANIFEST]` |
| `495` | `Mod_StPracticeField_Base` | `8` | `get_state, open_panel` | `[READY_IN_MANIFEST]` |
| `496` | `Mod_GodRank_Base` | `43` | `activity_state, apply_panel` | `[READY_IN_MANIFEST]` |
| `497` | `Mod_NewFunctionHerald_Base` | `5` | `get_info, get_award` | `[READY_IN_MANIFEST]` |
| `498` | `Mod_IconHideFunction_Base` | `3` | `get_info, hide_icon` | `[READY_IN_MANIFEST]` |
| `499` | `Mod_GodRankCrossing_Base` | `12` | `get_info, begin_crossing` | `[READY_IN_MANIFEST]` |
| `500` | `Mod_GodRankRank_Base` | `3` | `get_rank_list, worship` | `[READY_IN_MANIFEST]` |
| `501` | `Mod_ChatSet_Base` | `7` | `get_info, set_title` | `[READY_IN_MANIFEST]` |
| `502` | `Mod_GodRankHonor_Base` | `12` | `open_panel, achievement_info` | `[READY_IN_MANIFEST]` |
| `503` | `Mod_AskFairy_Base` | `8` | `get_recall_info, gain_recall_award` | `[READY_IN_MANIFEST]` |
| `504` | `Mod_RedBagWall_Base` | `7` | `get_panel_info, invite_friend` | `[READY_IN_MANIFEST]` |
| `505` | `Mod_StMouse_Base` | `9` | `feed_panel, feed` | `[READY_IN_MANIFEST]` |
| `506` | `Mod_ThanksgivingSpringFestival_Base` | `2` | `act_info, get_award` | `[READY_IN_MANIFEST]` |
| `507` | `Mod_NewServerWar_Base` | `18` | `get_race_step, get_standings` | `[READY_IN_MANIFEST]` |
| `508` | `Mod_NewMonthCard_Base` | `3` | `new_month_card_info, buy_new_month_card` | `[READY_IN_MANIFEST]` |
| `509` | `Mod_JobPlate_Base` | `3` | `open_panel, active_grid` | `[READY_IN_MANIFEST]` |
| `510` | `Mod_StrategyNote_Base` | `4` | `strategy_note_info, commit_strategy_note` | `[READY_IN_MANIFEST]` |
| `511` | `Mod_SaTrials_Base` | `11` | `get_panel_info, reset_trials` | `[READY_IN_MANIFEST]` |
| `512` | `Mod_ArmorRefine_Base` | `3` | `armor_refine_info, refine` | `[READY_IN_MANIFEST]` |
| `513` | `Mod_TeamPlatformRace_Base` | `47` | `activity_step, open_panel` | `[READY_IN_MANIFEST]` |
| `514` | `Mod_FightVirus_Base` | `9` | `fight_virus_info, contribute_info` | `[READY_IN_MANIFEST]` |
| `515` | `Mod_NewServerPray_Base` | `4` | `get_panel_info, pray_award` | `[READY_IN_MANIFEST]` |
| `516` | `Mod_NewStTravelShop_Base` | `4` | `get_panel_info, buy_item` | `[READY_IN_MANIFEST]` |
| `517` | `Mod_TreasureMouse_Base` | `12` | `get_activity_step, call_step_panel` | `[READY_IN_MANIFEST]` |
| `518` | `Mod_MainRoleFaXiang_Base` | `18` | `get_panel_info, refine_book` | `[READY_IN_MANIFEST]` |
| `519` | `Mod_StPoem_Base` | `7` | `question_panel, get_recommend` | `[READY_IN_MANIFEST]` |
| `520` | `Mod_WorldPoem_Base` | `8` | `activity_step, question_panel` | `[READY_IN_MANIFEST]` |
| `521` | `Mod_SaWorldTower_Base` | `7` | `get_open_status, get_panel_info` | `[READY_IN_MANIFEST]` |
| `522` | `Mod_WarSimulator_Base` | `14` | `war_simulator_info, save_role_info` | `[READY_IN_MANIFEST]` |
| `523` | `Mod_NewMutual_Base` | `9` | `open_panel, friend_list` | `[READY_IN_MANIFEST]` |
| `524` | `Mod_IdentifyTreasure_Base` | `6` | `get_open_status, get_panel_info` | `[READY_IN_MANIFEST]` |
| `525` | `Mod_BigRing_Base` | `9` | `open_panel, confirm_panel` | `[READY_IN_MANIFEST]` |
| `526` | `Mod_MemoryZone_Base` | `4` | `main_panel, back_panel` | `[READY_IN_MANIFEST]` |
| `527` | `Mod_MissionQuickFight_Base` | `3` | `get_quick_fight_info, start_quick_mission` | `[READY_IN_MANIFEST]` |
| `528` | `Mod_PlayerSetting_Base` | `3` | `setting_info, set_setting` | `[READY_IN_MANIFEST]` |
| `529` | `Mod_ThreeWorld_Base` | `6` | `get_status, get_login_info` | `[READY_IN_MANIFEST]` |
| `530` | `Mod_HumanWorldBossFight_Base` | `7` | `get_boss_info, rank_list` | `[READY_IN_MANIFEST]` |
| `531` | `Mod_HumanWorld_Base` | `50` | `big_map_panel, get_town_info` | `[READY_IN_MANIFEST]` |
| `532` | `Mod_FiveElementsDisk_Base` | `14` | `main_panel_info, upgrade` | `[READY_IN_MANIFEST]` |
| `533` | `Mod_ExploreHell_Base` | `63` | `open_match_panel, close_match_panel` | `[READY_IN_MANIFEST]` |
| `534` | `Mod_DragonAreaShop_Base` | `5` | `blessing_panel, enable_blessing` | `[READY_IN_MANIFEST]` |
| `535` | `Mod_NewPartnerStory_Base` | `7` | `open_main_panel, commit_option` | `[READY_IN_MANIFEST]` |
| `536` | `Mod_YinyangHall_Base` | `12` | `open_panel, level_up` | `[READY_IN_MANIFEST]` |
| `537` | `Mod_TreasureWish_Base` | `11` | `main_panel_info, invite_friend` | `[READY_IN_MANIFEST]` |
| `538` | `Mod_PartnerPresent_Base` | `4` | `open_panel, get_free_gift` | `[READY_IN_MANIFEST]` |
| `539` | `Mod_BestPartner_Base` | `13` | `get_status, get_panel_info` | `[READY_IN_MANIFEST]` |
| `540` | `Mod_LimitedTimeCharge_Base` | `9` | `open_panel, get_gift` | `[READY_IN_MANIFEST]` |
| `541` | `Mod_PreheatActivity_Base` | `4` | `get_panel_info, answer_question` | `[READY_IN_MANIFEST]` |
| `542` | `Mod_LinkLoginPresent_Base` | `2` | `open_panel, sign` | `[READY_IN_MANIFEST]` |
| `543` | `Mod_LinkLimitedSell_Base` | `4` | `open_panel, buy_gift` | `[READY_IN_MANIFEST]` |
| `544` | `Mod_LinkStoryGame_Base` | `3` | `open_panel, roll_dice` | `[READY_IN_MANIFEST]` |
| `545` | `Mod_LinkKillMonster_Base` | `16` | `panel_info, chapters_info` | `[READY_IN_MANIFEST]` |
| `546` | `Mod_SeasonScroll_Base` | `5` | `open_panel, get_target_award` | `[READY_IN_MANIFEST]` |
| `547` | `Mod_DataStatistics_Base` | `1` | `record_browser` | `[READY_IN_MANIFEST]` |
| `548` | `Mod_NewServerTalent_Base` | `8` | `get_status, get_panel_info` | `[READY_IN_MANIFEST]` |
| `549` | `Mod_StGodWelfare_Base` | `3` | `open_panel, get_award` | `[READY_IN_MANIFEST]` |
| `550` | `Mod_NewYearBlessing_Base` | `9` | `system_gift_state, get_system_gift` | `[READY_IN_MANIFEST]` |
| `551` | `Mod_GoldenTouchStone_Base` | `8` | `get_status, get_share_panel_info` | `[READY_IN_MANIFEST]` |
| `552` | `Mod_XiuzhenRealm_Base` | `5` | `main_panel, realm_panel` | `[READY_IN_MANIFEST]` |
| `553` | `Mod_CouponShop_Base` | `3` | `coupon_shop_info, add_item` | `[READY_IN_MANIFEST]` |
| `554` | `Mod_BuildHighBuilding_Base` | `6` | `get_panel_info, get_group_info` | `[READY_IN_MANIFEST]` |
| `555` | `Mod_WorldRaceRank_Base` | `2` | `rank_info, panel_info` | `[READY_IN_MANIFEST]` |
| `556` | `Mod_ResourceShow_Base` | `1` | `get_panel_info` | `[READY_IN_MANIFEST]` |
| `557` | `Mod_SunMoonBlessing_Base` | `9` | `main_panel, set_wish_item` | `[READY_IN_MANIFEST]` |
| `558` | `Mod_RedDot_Base` | `3` | `get_red_dot_list, notify_red_dot_status_change` | `[READY_IN_MANIFEST]` |
| `559` | `Mod_DebugGm_Base` | `4` | `help_info, cheat` | `[READY_IN_MANIFEST]` |
| `560` | `Mod_LinkShoppingBack_Base` | `4` | `panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `561` | `Mod_TenYearBigEvent_Base` | `3` | `open_panel, join_activity` | `[READY_IN_MANIFEST]` |
| `562` | `Mod_ImageSetting_Base` | `15` | `image_setting_info, image_set` | `[READY_IN_MANIFEST]` |
| `563` | `Mod_WishTemple_Base` | `8` | `panel_info, build` | `[READY_IN_MANIFEST]` |
| `564` | `Mod_TenYearMemory_Base` | `9` | `get_state, main_panel` | `[READY_IN_MANIFEST]` |
| `565` | `Mod_LunHuiChink_Base` | `4` | `get_info, merge_stone` | `[READY_IN_MANIFEST]` |
| `566` | `Mod_IllusionShrine_Base` | `2` | `open_panel, select_scene` | `[READY_IN_MANIFEST]` |
| `567` | `Mod_LinkageSkill_Base` | `2` | `linkage_skill_info, active_skill` | `[READY_IN_MANIFEST]` |
| `568` | `Mod_WealthCelebration_Base` | `9` | `self_code, get_code` | `[READY_IN_MANIFEST]` |
| `569` | `Mod_ChargeRepay_Base` | `2` | `charge_repay_info, get_award` | `[READY_IN_MANIFEST]` |
| `570` | `Mod_ConstellationStarPlate_Base` | `2` | `panel_info, light_star` | `[READY_IN_MANIFEST]` |
| `571` | `Mod_Sect_Base` | `9` | `panel_info, sect_list` | `[READY_IN_MANIFEST]` |
| `572` | `Mod_SectUtility_Base` | `18` | `sect_main_info, modify_sect_name` | `[READY_IN_MANIFEST]` |
| `574` | `Mod_Fairyland_Base` | `5` | `fairyland_info, fight` | `[READY_IN_MANIFEST]` |
| `575` | `Mod_SectLogin_Base` | `14` | `get_login_info, login` | `[READY_IN_MANIFEST]` |
| `576` | `Mod_SectMonster_Base` | `5` | `egg_panel_info, get_monster_list` | `[READY_IN_MANIFEST]` |
| `577` | `Mod_SectShop_Base` | `6` | `shop_info, buy_shop_item` | `[READY_IN_MANIFEST]` |
| `578` | `Mod_SectStunt_Base` | `18` | `area_panel, train_panel` | `[READY_IN_MANIFEST]` |
| `579` | `Mod_SectPracticeField_Base` | `17` | `contest_panel, start_fight` | `[READY_IN_MANIFEST]` |
| `580` | `Mod_BuildDream_Base` | `7` | `panel_info, build` | `[READY_IN_MANIFEST]` |
| `581` | `Mod_DragonToken_Base` | `3` | `panel_info, active` | `[READY_IN_MANIFEST]` |
| `582` | `Mod_NewBank_Base` | `9` | `open_panel, buy_fu` | `[READY_IN_MANIFEST]` |
| `583` | `Mod_GodWish_Base` | `4` | `panel_info, select_award` | `[READY_IN_MANIFEST]` |
| `584` | `Mod_NewPractice_Base` | `3` | `get_practice_info, collect_air` | `[READY_IN_MANIFEST]` |
| `585` | `Mod_NaturalTreasure_Base` | `13` | `panel_info, up_star` | `[READY_IN_MANIFEST]` |
| `586` | `Mod_RefineFurnace_Base` | `8` | `open_panel, select_type` | `[READY_IN_MANIFEST]` |
| `587` | `Mod_WarPowerFunds_Base` | `3` | `panel_info, buy_seq` | `[READY_IN_MANIFEST]` |
| `588` | `Mod_NewGroupon_Base` | `10` | `get_catelog_item, get_back_list` | `[READY_IN_MANIFEST]` |
| `589` | `Mod_HotItemRank_Base` | `11` | `catelog_item_rank, get_item_detail` | `[READY_IN_MANIFEST]` |
| `590` | `Mod_PartnerDivine_Base` | `5` | `panel_info, divine` | `[READY_IN_MANIFEST]` |
| `591` | `Mod_SectBonus_Base` | `3` | `open_panel, get_gift_record` | `[READY_IN_MANIFEST]` |
| `592` | `Mod_HelpFunds_Base` | `2` | `panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `593` | `Mod_SectWar_Base` | `13` | `get_state, panel_info` | `[READY_IN_MANIFEST]` |
| `594` | `Mod_TreasureHouse_Base` | `10` | `main_panel, select_panel` | `[READY_IN_MANIFEST]` |
| `595` | `Mod_KnowledgeQuiz_Base` | `5` | `open_panel, state_change` | `[READY_IN_MANIFEST]` |
| `596` | `Mod_SecretScroll_Base` | `14` | `main_scroll, set_show_flag` | `[READY_IN_MANIFEST]` |
| `597` | `Mod_WorldRank_Base` | `2` | `get_rank_list, get_self_value` | `[READY_IN_MANIFEST]` |
| `598` | `Mod_LianDongReturn_Base` | `3` | `panel_info, invite` | `[READY_IN_MANIFEST]` |
| `599` | `Mod_StarLetter_Base` | `12` | `star_letter_info, choose_star` | `[READY_IN_MANIFEST]` |
| `600` | `Mod_SnowDemon_Base` | `10` | `open_panel, choose_award_list` | `[READY_IN_MANIFEST]` |
| `601` | `Mod_NewCostTalent_Base` | `3` | `panel_info, draw` | `[READY_IN_MANIFEST]` |
| `602` | `Mod_TeamPk_Base` | `32` | `get_status, main_panel` | `[READY_IN_MANIFEST]` |
| `603` | `Mod_NewYearSignIn_Base` | `8` | `get_player_sign_in_info, get_sign_in_award` | `[READY_IN_MANIFEST]` |
| `604` | `Mod_PeachParty_Base` | `27` | `get_status, panel_info` | `[READY_IN_MANIFEST]` |
| `605` | `Mod_GujiFindTreasure_Base` | `5` | `get_buy_status, open_panel` | `[READY_IN_MANIFEST]` |
| `606` | `Mod_NewServerInherit_Base` | `18` | `new_server_inherit_state, new_server_panal` | `[READY_IN_MANIFEST]` |
| `607` | `Mod_TheChosenWish_Base` | `2` | `open_panel, get_player_list` | `[READY_IN_MANIFEST]` |
| `608` | `Mod_ClearClouds_Base` | `9` | `open_panel, big_award_list` | `[READY_IN_MANIFEST]` |
| `609` | `Mod_GameBugShow_Base` | `4` | `panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `610` | `Mod_YesterdayMemory_Base` | `5` | `panel_info, send_message` | `[READY_IN_MANIFEST]` |
| `611` | `Mod_RefineryWorkshop_Base` | `3` | `open_panel, set_item` | `[READY_IN_MANIFEST]` |
| `612` | `Mod_MonsterShop_Base` | `11` | `new_server_info, new_server_choose_award_list` | `[READY_IN_MANIFEST]` |
| `613` | `Mod_LandContract_Base` | `11` | `get_panel_info, get_achievement_info` | `[READY_IN_MANIFEST]` |
| `614` | `Mod_SoulDeploy_Base` | `61` | `super_deploy_list, up_deploy` | `[READY_IN_MANIFEST]` |
| `615` | `Mod_SoulAbyss_Base` | `9` | `soul_abyss_panel, soul_info` | `[READY_IN_MANIFEST]` |
| `616` | `Mod_AroundShop_Base` | `14` | `shop_panel, get_charge_fortune` | `[READY_IN_MANIFEST]` |
| `617` | `Mod_AnniversaryMarket_Base` | `6` | `market_panel, donate_panel` | `[READY_IN_MANIFEST]` |
| `618` | `Mod_LinkLotusRoad_Base` | `7` | `open_panel, get_award` | `[READY_IN_MANIFEST]` |
| `619` | `Mod_ProtectLotusLight_Base` | `6` | `main_panel_info, start` | `[READY_IN_MANIFEST]` |
| `620` | `Mod_FantasyStory_Base` | `9` | `main_panel_info, chapter_panel_info` | `[READY_IN_MANIFEST]` |
| `621` | `Mod_AnniVideo_Base` | `8` | `open_panel, complete_task` | `[READY_IN_MANIFEST]` |
| `622` | `Mod_ReturnNewserver_Base` | `12` | `main_panel, server_panel` | `[READY_IN_MANIFEST]` |
| `623` | `Mod_ZongziVote_Base` | `7` | `panel_info, select_camp` | `[READY_IN_MANIFEST]` |
| `624` | `Mod_TreasureRoad_Base` | `5` | `activity_info, open_panel` | `[READY_IN_MANIFEST]` |
| `625` | `Mod_RealItemOrder_Base` | `3` | `get_acceptor_info, modify_acceptor_info` | `[READY_IN_MANIFEST]` |
| `626` | `Mod_MatchShop_Base` | `2` | `open_panel, buy_shop_item` | `[READY_IN_MANIFEST]` |
| `627` | `Mod_TimeTemple_Base` | `7` | `panel_info, pray` | `[READY_IN_MANIFEST]` |
| `628` | `Mod_TokenSupply_Base` | `2` | `get_info, buy_token` | `[READY_IN_MANIFEST]` |
| `629` | `Mod_SwordsectRace_Base` | `9` | `activity_step, main_panel` | `[READY_IN_MANIFEST]` |
| `630` | `Mod_SwordsectRaceDeploy_Base` | `40` | `super_deploy_list, partner_list` | `[READY_IN_MANIFEST]` |
| `631` | `Mod_SummerPractice_Base` | `5` | `open_panel, get_award` | `[READY_IN_MANIFEST]` |
| `632` | `Mod_SummerLottery_Base` | `5` | `panel_info, choose_award_list` | `[READY_IN_MANIFEST]` |
| `633` | `Mod_PsychicInstrument_Base` | `3` | `panel_info, upgrade_level` | `[READY_IN_MANIFEST]` |
| `634` | `Mod_ThemeSong_Base` | `7` | `get_activity_step, listen_panel` | `[READY_IN_MANIFEST]` |
| `635` | `Mod_PracticeGuidance_Base` | `1` | `panel_info` | `[READY_IN_MANIFEST]` |
| `636` | `Mod_ActivityWeek_Base` | `1` | `open_activity` | `[READY_IN_MANIFEST]` |
| `637` | `Mod_WeekendRevelryGiftPack_Base` | `3` | `panel_info, get_award` | `[READY_IN_MANIFEST]` |
| `638` | `Mod_WeekendRevelryEntrust_Base` | `2` | `panel_info, set_auto_finish` | `[READY_IN_MANIFEST]` |
| `639` | `Mod_WeekendRevelryDiscount_Base` | `1` | `panel_info` | `[READY_IN_MANIFEST]` |
| `640` | `Mod_SeasonCard_Base` | `4` | `get_info, buy_card` | `[READY_IN_MANIFEST]` |
| `641` | `Mod_RegressionSpup_Base` | `4` | `get_status, panel_info` | `[READY_IN_MANIFEST]` |
| `642` | `Mod_RegressionInherit_Base` | `2` | `get_status, panel_info` | `[READY_IN_MANIFEST]` |
| `643` | `Mod_FinalTownForecast_Base` | `5` | `get_status, get_info` | `[READY_IN_MANIFEST]` |
| `644` | `Mod_ActiveRepay_Base` | `4` | `get_panel_info, apply_draw` | `[READY_IN_MANIFEST]` |
| `645` | `Mod_ShanhaiWorld_Base` | `13` | `get_login_info, login` | `[READY_IN_MANIFEST]` |
| `646` | `Mod_SkyPalace_Base` | `24` | `main_panel_info, break_through` | `[READY_IN_MANIFEST]` |
| `647` | `Mod_AlchemyStove_Base` | `7` | `get_panel_info, get_status` | `[READY_IN_MANIFEST]` |
| `648` | `Mod_TongTianTower_Base` | `13` | `panel_info, challenge` | `[READY_IN_MANIFEST]` |
| `649` | `Mod_CommonAchievement_Base` | `2` | `get_achievement_info, gain_achievement` | `[READY_IN_MANIFEST]` |
| `650` | `Mod_MidAutumnFeedback_Base` | `4` | `is_display_panel, open_panel` | `[READY_IN_MANIFEST]` |
| `651` | `Mod_LinlangPavilion_Base` | `8` | `open_panel, buy_item` | `[READY_IN_MANIFEST]` |
| `652` | `Mod_StVoid_Base` | `4` | `open_panel, like` | `[READY_IN_MANIFEST]` |
| `653` | `Mod_RecruitGift_Base` | `3` | `get_status, open_panel` | `[READY_IN_MANIFEST]` |
| `654` | `Mod_RefinePot_Base` | `8` | `refine_panel, from_item_list` | `[READY_IN_MANIFEST]` |
| `655` | `Mod_WealthGodBefallNew_Base` | `2` | `activity_info, open_box` | `[READY_IN_MANIFEST]` |
| `656` | `Mod_SoulPkRanking_Base` | `10` | `get_state, main_panel` | `[READY_IN_MANIFEST]` |
| `657` | `Mod_Gongfa_Base` | `13` | `main_panel, level_up` | `[READY_IN_MANIFEST]` |
| `658` | `Mod_WuFaField_Base` | `10` | `panel_info, draw` | `[READY_IN_MANIFEST]` |
| `659` | `Mod_DoubleElevenLiJuan_Base` | `2` | `get_panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `660` | `Mod_QatarWorldCup_Base` | `18` | `activity_state, main_panel` | `[READY_IN_MANIFEST]` |
| `661` | `Mod_YiChuiDingYin_Base` | `5` | `get_panel_info, knock` | `[READY_IN_MANIFEST]` |
| `662` | `Mod_SearchTreasureBox_Base` | `3` | `get_panel_info, choose_award` | `[READY_IN_MANIFEST]` |
| `663` | `Mod_ItemPalace_Base` | `6` | `main_panel, level_up` | `[READY_IN_MANIFEST]` |
| `664` | `Mod_FlashSale_Base` | `3` | `get_panel_info, buy` | `[READY_IN_MANIFEST]` |
| `665` | `Mod_MasterPractice_Base` | `10` | `main_panel, get_deploy_info` | `[READY_IN_MANIFEST]` |
| `666` | `Mod_NewsDisplay_Base` | `6` | `main_panel, get_award` | `[READY_IN_MANIFEST]` |
| `667` | `Mod_DressPlan_Base` | `5` | `main_panel, up_level` | `[READY_IN_MANIFEST]` |
| `668` | `Mod_SoulHuntDeploy_Base` | `46` | `super_deploy_list, partner_list` | `[READY_IN_MANIFEST]` |
| `669` | `Mod_SoulHunt_Base` | `19` | `get_activity_state, main_panel` | `[READY_IN_MANIFEST]` |
| `670` | `Mod_TimePromise_Base` | `6` | `main_panel, open_box` | `[READY_IN_MANIFEST]` |
| `671` | `Mod_MemoryClock_Base` | `4` | `main_panel, activate` | `[READY_IN_MANIFEST]` |
| `672` | `Mod_SoulHuntBlessGift_Base` | `3` | `main_panel_info, active` | `[READY_IN_MANIFEST]` |
| `673` | `Mod_RabbitPresent_Base` | `6` | `open_panel, get_free_carrot` | `[READY_IN_MANIFEST]` |
| `674` | `Mod_SfMissionMonth_Base` | `2` | `get_panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `675` | `Mod_FreeShop_Base` | `5` | `shop_panel, self_buy_records` | `[READY_IN_MANIFEST]` |
| `676` | `Mod_ShuilingInvitation_Base` | `4` | `main_panel_info, unlock_stage` | `[READY_IN_MANIFEST]` |
| `677` | `Mod_HermitHome_Base` | `19` | `main_panel, pour_soul` | `[READY_IN_MANIFEST]` |
| `678` | `Mod_WuFaFieldActivity_Base` | `9` | `draw_times_award_info, get_draw_times_award` | `[READY_IN_MANIFEST]` |
| `679` | `Mod_AnniversaryWinner_Base` | `27` | `activity_step, top_race_main_panel` | `[READY_IN_MANIFEST]` |
| `680` | `Mod_CommonScoreExchange_Base` | `3` | `luck_score_panel, gain_luck_award` | `[READY_IN_MANIFEST]` |
| `681` | `Mod_Thanksgiving_Base` | `2` | `act_info, get_award` | `[READY_IN_MANIFEST]` |
| `682` | `Mod_LinkLimitedSellNew_Base` | `6` | `open_panel, act` | `[READY_IN_MANIFEST]` |
| `683` | `Mod_FengyunChallenge_Base` | `11` | `main_panel, buy_challenge_times` | `[READY_IN_MANIFEST]` |
| `684` | `Mod_FriendsSent_Base` | `4` | `main_panel, open_letter` | `[READY_IN_MANIFEST]` |
| `685` | `Mod_AnniversaryTower_Base` | `5` | `open_panel, get_award` | `[READY_IN_MANIFEST]` |
| `686` | `Mod_AnniversaryCelebration_Base` | `3` | `main_panel, use_fireworks` | `[READY_IN_MANIFEST]` |
| `687` | `Mod_CelebrationRank_Base` | `2` | `get_rank, like` | `[READY_IN_MANIFEST]` |
| `688` | `Mod_AnniversaryShop_Base` | `3` | `shop_list, shop_item_info` | `[READY_IN_MANIFEST]` |
| `689` | `Mod_AnniversaryTable_Base` | `2` | `main_panel, get_ingot` | `[READY_IN_MANIFEST]` |
| `690` | `Mod_EndlessBox_Base` | `6` | `panel_info, open_box` | `[READY_IN_MANIFEST]` |
| `691` | `Mod_AnniversaryDemon_Base` | `9` | `activity_panel, play_story` | `[READY_IN_MANIFEST]` |
| `692` | `Mod_EvilInvade_Base` | `4` | `panel_info, set_play_state` | `[READY_IN_MANIFEST]` |
| `693` | `Mod_Eudemons_Base` | `11` | `panel_info, get_skins` | `[READY_IN_MANIFEST]` |
| `694` | `Mod_PhantomGemLottery_Base` | `3` | `panel_info, find` | `[READY_IN_MANIFEST]` |
| `695` | `Mod_PhantomGem_Base` | `5` | `bag_panel, step_up_panel` | `[READY_IN_MANIFEST]` |
| `696` | `Mod_EudemonsInvade_Base` | `7` | `panel_info, get_now_stage` | `[READY_IN_MANIFEST]` |
| `697` | `Mod_LotusLantern_Base` | `5` | `bless_panel, select_award` | `[READY_IN_MANIFEST]` |
| `698` | `Mod_SummerThemedGift_Base` | `3` | `panel_info, buy_gift` | `[READY_IN_MANIFEST]` |
| `699` | `Mod_SummerShop_Base` | `3` | `panel_info, exchange` | `[READY_IN_MANIFEST]` |
| `700` | `Mod_StuntConfig_Base` | `2` | `get_role_stunt_config, config_role_stunt` | `[READY_IN_MANIFEST]` |
| `701` | `Mod_StateRecord_Base` | `2` | `get_state, set_state` | `[READY_IN_MANIFEST]` |
| `702` | `Mod_TongTianTowerHire_Base` | `8` | `open_panel, view_role_detail` | `[READY_IN_MANIFEST]` |
| `703` | `Mod_RiverGodTrial_Base` | `4` | `panel_info, get_task_award` | `[READY_IN_MANIFEST]` |
| `704` | `Mod_TianJianConn_Base` | `5` | `tian_jian_conn_state, question_panel_info` | `[READY_IN_MANIFEST]` |
| `705` | `Mod_RepressDemonTower_Base` | `9` | `panel_info, challenge` | `[READY_IN_MANIFEST]` |
| `706` | `Mod_ChargeActivityGuide_Base` | `1` | `main_panel` | `[READY_IN_MANIFEST]` |
| `707` | `Mod_CatGold_Base` | `5` | `cat_gold_info, buy_gift` | `[READY_IN_MANIFEST]` |
| `708` | `Mod_FairyGame_Base` | `8` | `open_panel, draw_card` | `[READY_IN_MANIFEST]` |
| `709` | `Mod_HeavenlyJadeTrading_Base` | `13` | `main_panel, buy_item` | `[READY_IN_MANIFEST]` |
| `710` | `Mod_TreasuresBox_Base` | `10` | `main_panel, choose_award_panel` | `[READY_IN_MANIFEST]` |
| `711` | `Mod_WuFaFieldBattlepass_Base` | `5` | `main_panel, unlock` | `[READY_IN_MANIFEST]` |
| `712` | `Mod_OnlineReward_Base` | `2` | `main_panel, one_key_get` | `[READY_IN_MANIFEST]` |
| `713` | `Mod_FirstChargeReward_Base` | `3` | `get_status, main_panel` | `[READY_IN_MANIFEST]` |
| `714` | `Mod_FairylandDispatch_Base` | `16` | `main_panel, task_panel` | `[READY_IN_MANIFEST]` |
| `715` | `Mod_RaceOrder_Base` | `4` | `main_panel, unlock` | `[READY_IN_MANIFEST]` |
| `716` | `Mod_ImmortalLeague_Base` | `14` | `main_panel, get_realm_info` | `[READY_IN_MANIFEST]` |
| `717` | `Mod_ConsumeRevel_Base` | `2` | `main_panel, get_li_quan` | `[READY_IN_MANIFEST]` |
| `718` | `Mod_AllStarQualify_Base` | `1` | `get_self_rank` | `[READY_IN_MANIFEST]` |
| `719` | `Mod_AuctionHouse_Base` | `10` | `open_auction_panel, close_auction_panel` | `[READY_IN_MANIFEST]` |
| `720` | `Mod_NineStarsRow_Base` | `4` | `main_panel, upgrade` | `[READY_IN_MANIFEST]` |
| `721` | `Mod_ExtremeTrial_Base` | `32` | `main_panel_info, task_panel_info` | `[READY_IN_MANIFEST]` |
| `722` | `Mod_WinterScratchCard_Base` | `3` | `panel_info, open` | `[READY_IN_MANIFEST]` |
| `723` | `Mod_MoneyRolling_Base` | `2` | `open_panel, lottery` | `[READY_IN_MANIFEST]` |
| `724` | `Mod_FourImage_Base` | `15` | `open_panel, block_pack` | `[READY_IN_MANIFEST]` |
| `725` | `Mod_YearVote_Base` | `13` | `main_panel, get_race_players` | `[READY_IN_MANIFEST]` |
| `726` | `Mod_NewYearComingCracker_Base` | `4` | `main_panel, light` | `[READY_IN_MANIFEST]` |
| `727` | `Mod_NewYearComingLuckyFish_Base` | `5` | `main_panel, draw_number` | `[READY_IN_MANIFEST]` |
| `728` | `Mod_PalaceCompetition_Base` | `13` | `activity_step, camp_pick_panel` | `[READY_IN_MANIFEST]` |
| `729` | `Mod_PalaceCompetitionFinals_Base` | `15` | `main_info, weed_out_info` | `[READY_IN_MANIFEST]` |
| `730` | `Mod_ChargeBackSpecial_Base` | `5` | `get_info, get_award` | `[READY_IN_MANIFEST]` |
| `731` | `Mod_NewDunhuangTreasure_Base` | `6` | `get_panel_info, choose_topic` | `[READY_IN_MANIFEST]` |
| `732` | `Mod_ChenlongPray_Base` | `6` | `get_panel_info, pray` | `[READY_IN_MANIFEST]` |
| `733` | `Mod_CollectFunds_Base` | `3` | `panel_info, buy_seq` | `[READY_IN_MANIFEST]` |
| `734` | `Mod_ExhibitionGame_Base` | `3` | `main_panel, support` | `[READY_IN_MANIFEST]` |
| `735` | `Mod_VoucherShop_Base` | `5` | `main_panel, buy_privilege` | `[READY_IN_MANIFEST]` |
| `736` | `Mod_XuantianTreasureRecord_Base` | `4` | `get_activity_status, main_panel` | `[READY_IN_MANIFEST]` |
| `737` | `Mod_VipLimitGift_Base` | `4` | `open_panel, get_free_award` | `[READY_IN_MANIFEST]` |
| `738` | `Mod_NewStRank_Base` | `6` | `rank_info, open_panel` | `[READY_IN_MANIFEST]` |
| `739` | `Mod_SeasonRanking_Base` | `9` | `get_self_info, get_top_rank_info` | `[READY_IN_MANIFEST]` |
| `740` | `Mod_MysticalTreasure_Base` | `3` | `get_panel_info, get_mission_time` | `[READY_IN_MANIFEST]` |
| `741` | `Mod_DemonKingBattle_Base` | `8` | `main_info, move_role` | `[READY_IN_MANIFEST]` |
| `742` | `Mod_GardenParty_Base` | `6` | `open_panel, select_big_award` | `[READY_IN_MANIFEST]` |
| `743` | `Mod_QingMingRespect_Base` | `8` | `get_panel_info, open_poetry` | `[READY_IN_MANIFEST]` |
| `744` | `Mod_RareTreasure_Base` | `2` | `open_panel, exchange` | `[READY_IN_MANIFEST]` |
| `745` | `Mod_NewAroundShop_Base` | `5` | `shop_panel, lottery` | `[READY_IN_MANIFEST]` |
| `746` | `Mod_PracticeSoulLaw_Base` | `8` | `get_player_panel_info, get_golden_dan_panel_info` | `[READY_IN_MANIFEST]` |
| `747` | `Mod_YunyinFengxing_Base` | `6` | `get_meridian_info, unlock_step` | `[READY_IN_MANIFEST]` |
| `748` | `Mod_Monoploy_Base` | `13` | `main_panel, roll_dice` | `[READY_IN_MANIFEST]` |
| `749` | `Mod_YuanBaoDoublingMachine_Base` | `3` | `get_panel_info, yuan_bao_doubling` | `[READY_IN_MANIFEST]` |
| `750` | `Mod_QiankunHall_Base` | `3` | `get_panel_info, buy_item` | `[READY_IN_MANIFEST]` |
| `751` | `Mod_DreamWorld_Base` | `7` | `main_panel, view_story` | `[READY_IN_MANIFEST]` |
| `752` | `Mod_XiandaoTongyou_Base` | `12` | `get_state, get_team_list` | `[READY_IN_MANIFEST]` |
| `753` | `Mod_NewServerMatch_Base` | `8` | `get_match_open_time, get_panel_info` | `[READY_IN_MANIFEST]` |
| `754` | `Mod_NewServerWishTree_Base` | `1` | `activity_info` | `[READY_IN_MANIFEST]` |
| `755` | `Mod_PetImmortalDomain_Base` | `26` | `get_state, sect_domain_list` | `[READY_IN_MANIFEST]` |
| `756` | `Mod_FreePartner_Base` | `8` | `main_panel, choose_list` | `[READY_IN_MANIFEST]` |
| `757` | `Mod_Traders_Base` | `8` | `get_panel_info, daily_and_term_flag` | `[READY_IN_MANIFEST]` |
| `758` | `Mod_MysticCompanionMySoul_Base` | `6` | `get_panel_info, change_soul_lock_state` | `[READY_IN_MANIFEST]` |
| `759` | `Mod_ElixirFuse_Base` | `2` | `fuse, up_fuse_lv_limit` | `[READY_IN_MANIFEST]` |
| `760` | `Mod_MysticPartner_Base` | `26` | `main_panel, attribute_panel` | `[READY_IN_MANIFEST]` |
| `761` | `Mod_PartnerAppearance_Base` | `4` | `panel_info, activate` | `[READY_IN_MANIFEST]` |
| `762` | `Mod_MysticCapture_Base` | `6` | `click_enter_hunt, enter_hunt` | `[READY_IN_MANIFEST]` |
| `763` | `Mod_CosmosFight_Base` | `20` | `get_state, choose_cornerstone_road` | `[READY_IN_MANIFEST]` |
| `764` | `Mod_CosmosFightDeploy_Base` | `40` | `super_deploy_list, partner_list` | `[READY_IN_MANIFEST]` |
| `765` | `Mod_NewSectShop_Base` | `5` | `gift_shop_panel, buy_gift_shop_item` | `[READY_IN_MANIFEST]` |
| `766` | `Mod_GardenTreasure_Base` | `6` | `main_panel, find_treasure` | `[READY_IN_MANIFEST]` |
| `767` | `Mod_TopMysticPartner_Base` | `2` | `get_rank, get_self_score` | `[READY_IN_MANIFEST]` |
| `768` | `Mod_SummerCream_Base` | `10` | `get_panel_info, get_ingredient` | `[READY_IN_MANIFEST]` |
| `769` | `Mod_SupremeVip_Base` | `4` | `get_vip_data, open_panel` | `[READY_IN_MANIFEST]` |
| `770` | `Mod_AncientRealm_Base` | `34` | `get_state, get_sect_team_list` | `[READY_IN_MANIFEST]` |
| `771` | `Mod_AncientRealmDeploy_Base` | `40` | `super_deploy_list, partner_list` | `[READY_IN_MANIFEST]` |
| `772` | `Mod_AncientRealmUtility_Base` | `12` | `attribute_panel, skill_panel` | `[READY_IN_MANIFEST]` |
| `773` | `Mod_Questionnaire_Base` | `3` | `get_vote_state, get_vote_info` | `[READY_IN_MANIFEST]` |
| `774` | `Mod_GuRenXiangFeng_Base` | `6` | `get_my_info, get_resident_info` | `[READY_IN_MANIFEST]` |
| `775` | `Mod_InviteLuxuryGift_Base` | `2` | `panel_info, luck_draw` | `[READY_IN_MANIFEST]` |
| `776` | `Mod_ReturnBox_Base` | `3` | `get_panel_info, get_ingot_award` | `[READY_IN_MANIFEST]` |
| `777` | `Mod_GrxfLuckLottery_Base` | `4` | `panel_info, buy_gift` | `[READY_IN_MANIFEST]` |
| `778` | `Mod_ReturnBp_Base` | `4` | `main_panel, unlock_line` | `[READY_IN_MANIFEST]` |
| `779` | `Mod_DragonTreasure_Base` | `4` | `main_panel, select_pray_award` | `[READY_IN_MANIFEST]` |
| `780` | `Mod_FortuneGift_Base` | `3` | `get_panel_info, get_award` | `[READY_IN_MANIFEST]` |
| `781` | `Mod_AutumnMine_Base` | `3` | `main_panel, select_big_award` | `[READY_IN_MANIFEST]` |
| `782` | `Mod_GlimFestival_Base` | `5` | `main_panel, get_award` | `[READY_IN_MANIFEST]` |
| `783` | `Mod_NewSkyLanternBless_Base` | `13` | `get_activity_time, get_bless_rank` | `[READY_IN_MANIFEST]` |
| `784` | `Mod_NationaldayCheckin2024_Base` | `4` | `main_panel, sign_in` | `[READY_IN_MANIFEST]` |
| `785` | `Mod_NationaldayExchange2024_Base` | `3` | `main_panel, exchange` | `[READY_IN_MANIFEST]` |
| `786` | `Mod_HeavenTreasure_Base` | `6` | `get_panel_info, choose_award` | `[READY_IN_MANIFEST]` |
| `787` | `Mod_OftenUsePartner_Base` | `2` | `get_panel_info, set_often_use_flag` | `[READY_IN_MANIFEST]` |
| `788` | `Mod_ActivityOrder_Base` | `4` | `get_panel, unlock` | `[READY_IN_MANIFEST]` |
| `789` | `Mod_PartnerGift_Base` | `4` | `task_panel, get_task_award` | `[READY_IN_MANIFEST]` |
| `790` | `Mod_MySoulBook_Base` | `4` | `get_book_panel, get_capture_award` | `[READY_IN_MANIFEST]` |
| `791` | `Mod_HeroesBattleUtility_Base` | `12` | `activity_step, panel_team_up` | `[READY_IN_MANIFEST]` |
| `792` | `Mod_HeroesBattleScoreRace_Base` | `13` | `score_race_panel, change_member_position` | `[READY_IN_MANIFEST]` |
| `793` | `Mod_HeroesBattleCupRace_Base` | `10` | `cup_panel, bet_panel` | `[READY_IN_MANIFEST]` |
| `794` | `Mod_WanfaWorld_Base` | `12` | `get_login_info, login` | `[READY_IN_MANIFEST]` |
| `795` | `Mod_StarryClash_Base` | `5` | `get_panel_info, get_score_award` | `[READY_IN_MANIFEST]` |
| `796` | `Mod_AmagicEquip_Base` | `15` | `panel_info, item_info` | `[READY_IN_MANIFEST]` |
| `797` | `Mod_EndlessExpedition_Base` | `28` | `mission_panel, mission_info` | `[READY_IN_MANIFEST]` |
| `798` | `Mod_WealthyFortune_Base` | `3` | `get_panel_info, get_return_ingot` | `[READY_IN_MANIFEST]` |
| `799` | `Mod_GlazePavilion_Base` | `9` | `get_state, main_panel_info` | `[READY_IN_MANIFEST]` |
| `800` | `Mod_GotoWanfa_Base` | `3` | `open_panel, fly_up` | `[READY_IN_MANIFEST]` |
| `801` | `Mod_TombArtifacts_Base` | `15` | `get_state, main_panel_info` | `[READY_IN_MANIFEST]` |
| `802` | `Mod_PartnerSale_Base` | `6` | `is_open, panel_info` | `[READY_IN_MANIFEST]` |
| `803` | `Mod_PartnerSaleGift_Base` | `4` | `is_open, panel_info` | `[READY_IN_MANIFEST]` |
| `804` | `Mod_PartnerSoulArray_Base` | `17` | `is_func_open, smelt_panel_info` | `[READY_IN_MANIFEST]` |
| `805` | `Mod_LetterCollection_Base` | `3` | `get_state, panel_info` | `[READY_IN_MANIFEST]` |
| `806` | `Mod_DollCollection_Base` | `7` | `get_state, panel_info` | `[READY_IN_MANIFEST]` |
| `807` | `Mod_SnakeTurntable_Base` | `11` | `main_panel, lottery` | `[READY_IN_MANIFEST]` |
| `808` | `Mod_FortuneBox_Base` | `5` | `is_open, panel_info` | `[READY_IN_MANIFEST]` |
| `809` | `Mod_GodDaily_Base` | `13` | `is_func_open, panle_info` | `[READY_IN_MANIFEST]` |
| `810` | `Mod_SpringFestivalSnake_Base` | `1` | `panel_info` | `[READY_IN_MANIFEST]` |
| `811` | `Mod_TimeFortune_Base` | `5` | `panel_info, get_charge_award` | `[READY_IN_MANIFEST]` |
| `812` | `Mod_LineAwards_Base` | `5` | `panel_info, start_round` | `[READY_IN_MANIFEST]` |
| `813` | `Mod_LimitedTimeBox_Base` | `4` | `get_panel_info, buy_gift` | `[READY_IN_MANIFEST]` |
| `814` | `Mod_DeviceBindRewards_Base` | `7` | `get_bind_info, send_verify_code` | `[READY_IN_MANIFEST]` |
| `815` | `Mod_CollectionBooklets_Base` | `34` | `sect_info, sect_rank` | `[READY_IN_MANIFEST]` |
| `816` | `Mod_WelcomeGift_Base` | `4` | `is_activity_open, get_panel_info` | `[READY_IN_MANIFEST]` |
| `817` | `Mod_FunSevenDays_Base` | `8` | `is_activity_open, get_panel_info` | `[READY_IN_MANIFEST]` |
| `818` | `Mod_AbyssClash_Base` | `11` | `is_func_open, step1_panel_info` | `[READY_IN_MANIFEST]` |
| `819` | `Mod_FzqLottery_Base` | `3` | `get_panel_info, draw_award` | `[READY_IN_MANIFEST]` |
| `820` | `Mod_AnniversaryCelebrationFairy_Base` | `2` | `open_panel, get_level_award` | `[READY_IN_MANIFEST]` |
| `821` | `Mod_FourteenAnniversaryGift_Base` | `3` | `get_panel_info, get_free_gift` | `[READY_IN_MANIFEST]` |
| `822` | `Mod_FateRoad_Base` | `11` | `main_info, theory_info` | `[READY_IN_MANIFEST]` |
| `823` | `Mod_CloudTreasury_Base` | `2` | `get_panel_info, gain_award` | `[READY_IN_MANIFEST]` |
| `824` | `Mod_SeasonEmperorField_Base` | `18` | `func_is_open, field_overview` | `[READY_IN_MANIFEST]` |
| `825` | `Mod_MaritimeTrade_Base` | `23` | `panel_info, open_box` | `[READY_IN_MANIFEST]` |
| `826` | `Mod_IslandFishing_Base` | `15` | `panel_info, fishing` | `[READY_IN_MANIFEST]` |
| `827` | `Mod_LotusBlessing_Base` | `5` | `get_panel_info, select_award` | `[READY_IN_MANIFEST]` |
| `828` | `Mod_GoldenRoad_Base` | `3` | `panel_info, get_award` | `[READY_IN_MANIFEST]` |
| `829` | `Mod_IslandSummerOrder_Base` | `5` | `panel_info, get_award` | `[READY_IN_MANIFEST]` |
| `830` | `Mod_IslandSummerStore_Base` | `3` | `panel_info, exchange_award` | `[READY_IN_MANIFEST]` |
| `831` | `Mod_SxdTvSeriesVideoshow_Base` | `3` | `panel_info, set_played` | `[READY_IN_MANIFEST]` |
| `832` | `Mod_SxdTvSeriesStart_Base` | `3` | `panel_info, complete` | `[READY_IN_MANIFEST]` |
| `833` | `Mod_SxdTvSeriesCalendar_Base` | `2` | `panel_info, get_award` | `[READY_IN_MANIFEST]` |
| `834` | `Mod_SxdTvSeriesDraw_Base` | `2` | `panel_info, draw` | `[READY_IN_MANIFEST]` |
| `835` | `Mod_MartialRaceDeploy_Base` | `51` | `attribute_panel, attribute_upgrade` | `[READY_IN_MANIFEST]` |
| `836` | `Mod_NewPlayerGuide_Base` | `22` | `panel_info, gain_total_award` | `[READY_IN_MANIFEST]` |
| `837` | `Mod_MartialRaceScoreStep_Base` | `21` | `get_race_step, apply_panel` | `[READY_IN_MANIFEST]` |
| `838` | `Mod_MartialRaceGrabStep_Base` | `12` | `panel_info, grab_list` | `[READY_IN_MANIFEST]` |
| `839` | `Mod_RoleAwakeSoul_Base` | `4` | `get_panel_info, soul_add_exp` | `[READY_IN_MANIFEST]` |
| `840` | `Mod_EternalGamesPresent_Base` | `6` | `main_info, worship` | `[READY_IN_MANIFEST]` |
| `841` | `Mod_SandTreasure_Base` | `9` | `get_panle_info, skip_anim` | `[READY_IN_MANIFEST]` |
| `842` | `Mod_DestinySword_Base` | `18` | `panel_info, sword_panel_info` | `[READY_IN_MANIFEST]` |
| `843` | `Mod_DiceRewards_Base` | `5` | `panel_info, roll_dice` | `[READY_IN_MANIFEST]` |
| `844` | `Mod_ItemConvert_Base` | `2` | `panel_info, convert` | `[READY_IN_MANIFEST]` |
| `845` | `Mod_JiyuanguixuWorld_Base` | `12` | `get_login_info, login` | `[READY_IN_MANIFEST]` |
| `846` | `Mod_EraTreasureShop_Base` | `3` | `get_now_season, get_panel_info` | `[READY_IN_MANIFEST]` |
| `847` | `Mod_EraTreasureGift_Base` | `3` | `get_panel_info, buy_gift` | `[READY_IN_MANIFEST]` |
| `848` | `Mod_EraTreasureOrder_Base` | `7` | `get_panel_info, get_award` | `[READY_IN_MANIFEST]` |
| `849` | `Mod_EraRank_Base` | `5` | `get_self_info, get_top_rank_info` | `[READY_IN_MANIFEST]` |
| `850` | `Mod_EraMainPanel_Base` | `5` | `panel_info, get_award` | `[READY_IN_MANIFEST]` |
| `851` | `Mod_EraRebirthLandAttr_Base` | `10` | `get_now_season, get_panel_info` | `[READY_IN_MANIFEST]` |
| `852` | `Mod_EraRebirthLandAuto_Base` | `16` | `get_panel_info, start_auto` | `[READY_IN_MANIFEST]` |
| `853` | `Mod_EraInfiniteMission_Base` | `11` | `get_now_season, get_panel_info` | `[READY_IN_MANIFEST]` |
| `854` | `Mod_EraInfiniteMissionDeploy_Base` | `47` | `deploy_red_dot, super_deploy_list` | `[READY_IN_MANIFEST]` |
| `855` | `Mod_EraYanJieMission_Base` | `1` | `get_mission_list` | `[READY_IN_MANIFEST]` |
| `856` | `Mod_GemMaster_Base` | `5` | `panel_info, throw_gem` | `[READY_IN_MANIFEST]` |
| `857` | `Mod_SxdTvSeriesQuiz_Base` | `3` | `panel_info, question_panel` | `[READY_IN_MANIFEST]` |
| `859` | `Mod_CultivationCardGame_Base` | `18` | `panel_info, submit_group` | `[READY_IN_MANIFEST]` |
| `860` | `Mod_StrategyPost_Base` | `1` | `panel_info` | `[READY_IN_MANIFEST]` |
| `861` | `Mod_DaoistFellowCaller_Base` | `4` | `panel_info, unbind` | `[READY_IN_MANIFEST]` |
| `862` | `Mod_DaoistFellowRecipient_Base` | `6` | `panel_info, get_task_award` | `[READY_IN_MANIFEST]` |
| `863` | `Mod_SectMindset_Base` | `18` | `comprehen_panel, skill_list` | `[READY_IN_MANIFEST]` |
| `864` | `Mod_BringGoodNews_Base` | `7` | `panel_info, draw` | `[READY_IN_MANIFEST]` |
| `865` | `Mod_FortuneRun_Base` | `11` | `get_panel_info, use_item` | `[READY_IN_MANIFEST]` |
| `866` | `Mod_EraCreationRealm_Base` | `14` | `get_now_season, get_panel_info` | `[READY_IN_MANIFEST]` |
| `867` | `Mod_DeployCopy_Base` | `6` | `player_info, my_save_deploy_info` | `[READY_IN_MANIFEST]` |
| `868` | `Mod_StrategyPostFunc_Base` | `4` | `fun_panel_info, gain_fun_introduction_award` | `[READY_IN_MANIFEST]` |
| `869` | `Mod_SectMeritHall_Base` | `6` | `get_panel_info, logistics_panel` | `[READY_IN_MANIFEST]` |
| `870` | `Mod_SectBlessLand_Base` | `21` | `get_step, get_panel_info` | `[READY_IN_MANIFEST]` |
| `871` | `Mod_StarSummon_Base` | `8` | `panel_info, select_pool` | `[READY_IN_MANIFEST]` |
| `872` | `Mod_HeavenCalculate_Base` | `6` | `get_panel_info, bet` | `[READY_IN_MANIFEST]` |
| `873` | `Mod_AnniversaryPenMount_Base` | `12` | `get_panel_info, select_draw_award_info` | `[READY_IN_MANIFEST]` |
| `874` | `Mod_AnniversaryRewards_Base` | `3` | `get_panel_info, buy_store` | `[READY_IN_MANIFEST]` |
| `875` | `Mod_AnniversaryGold_Base` | `3` | `get_panel_info, draw` | `[READY_IN_MANIFEST]` |
| `876` | `Mod_EraSuperSport_Base` | `14` | `is_func_open, main_panel` | `[READY_IN_MANIFEST]` |
| `877` | `Mod_RareShop_Base` | `2` | `main_panel, exchange` | `[READY_IN_MANIFEST]` |
| `878` | `Mod_NewLuckyStore_Base` | `7` | `is_func_open, black_shop_panel` | `[READY_IN_MANIFEST]` |
| `879` | `Mod_RechargeShopActivity_Base` | `6` | `panel_info, get_task_award` | `[READY_IN_MANIFEST]` |
| `880` | `Mod_EudemonsStone_Base` | `9` | `is_func_open, get_panel_info` | `[READY_IN_MANIFEST]` |
| `881` | `Mod_EudemonsStoneShop_Base` | `3` | `panel_info, buy_stone` | `[READY_IN_MANIFEST]` |
| `882` | `Mod_EraLunHuiAlbum_Base` | `6` | `panel_info, get_task_info` | `[READY_IN_MANIFEST]` |
| `883` | `Mod_SectAllianceRank_Base` | `1` | `panel_info` | `[READY_IN_MANIFEST]` |
| `884` | `Mod_SectAlliance_Base` | `26` | `get_now_season, top_sect_panel` | `[READY_IN_MANIFEST]` |
| `885` | `Mod_RechargeVoucher_Base` | `2` | `panel_info, use_voucher` | `[READY_IN_MANIFEST]` |
| `886` | `Mod_EraRepressDemonTower_Base` | `10` | `panel_info, challenge` | `[READY_IN_MANIFEST]` |
| `887` | `Mod_HermitObject_Base` | `4` | `get_panel_info, object_panel_info` | `[READY_IN_MANIFEST]` |
| `888` | `Mod_EraImmortalLeague_Base` | `16` | `main_panel, get_realm_info` | `[READY_IN_MANIFEST]` |
| `889` | `Mod_EraImmortalLeagueDeploy_Base` | `47` | `deploy_red_dot, super_deploy_list` | `[READY_IN_MANIFEST]` |
| `890` | `Mod_FunctionBlock_Base` | `1` | `function_block_list` | `[READY_IN_MANIFEST]` |
| `891` | `Mod_ImmortalMerchant_Base` | `23` | `get_step, get_panel_info` | `[READY_IN_MANIFEST]` |

---

## 4. 二次开发与代码契约使用规范

在利用本元数据库与生成器进行自动化功能扩展时：
1. **禁止直接硬编码 Mod/Act 魔法数字**：优先通过 `scripts/protocol_codegen.py --mod <ID>` 生成标准契约类或引入常量；
2. **利用 `resolve_field_type_desc` 保证空安全**：生成的类均自带 `encode_payload()` 与 `decode()`，与网络层 `SXDClient.request()` 无缝契合；
3. **安全红线防御**：在调用包含元宝（`Ingot`）、高价值消耗品（`Coins`、`Gold`）的协议动作时，务必遵从安全防护规则添加前置卫语句防御。

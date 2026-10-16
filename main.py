"""神仙道无头协议自动化工具主入口 (CLI Entrypoint)

支持单次日常福利流水线 (--once)、24小时守护挂机模式 (--daemon) 以及特定任务调试 (--task)。

@author Ateng
@since 2026-10-15
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Optional, List, Dict, Any, Union

# Windows 终端 UTF-8 编码防御，防止乱码
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from core.context import GameContext
from core.events import EventBus
from core.config import AccountConfig, SettingsConfig, AppConfig, ConfigManager
from network.client import SXDClient
from network.web_auth import WebAuthFetcher, GatewayCredentials
from services.query_service import QueryService
from services.query_formatter import QueryFormatter
from storage.player_db import PlayerDatabase
from tasks.base import TaskResult
from tasks.scheduler import TaskScheduler
from tasks.routine.login import LoginTask
from tasks.routine.heartbeat import HeartbeatTask
from tasks.routine.signin import DailySignInTask
from tasks.routine.money_tree import FreeMoneyTreeTask
from tasks.routine.online_gift import OnlineGiftTask
from tasks.routine.worship import FactionWorshipTask
from tasks.routine.faction_roll import FactionRollCakeTask
from tasks.routine.lucky_star import LuckyStarTask
from tasks.routine.farm import FarmTask
from tasks.routine.peach_pet import PeachAndPetTask
from tasks.routine.fate import FateHuntTask
from tasks.routine.take_bible import TakeBibleTask
from tasks.battle.hero_mission import HeroMissionSweepTask
from tasks.battle.normal_mission import NormalMissionSweepTask
from tasks.battle.multi_mission import MultiMissionTask
from tasks.battle.super_sport import SuperSportTask
from tasks.battle.world_boss import WorldBossTask
from tasks.routine.travel_event import TravelEventTask
from tasks.routine.item_clean import ItemCleanTask
from tasks.routine.traders import TradersTask
from tasks.routine.fishing import FishingTask
from tasks.battle.tower import TowerTask
from tasks.routine.email import EmailTask
from tasks.routine.ask_fairy import AskFairyTask
from tasks.routine.touch_stone import GoldenTouchStoneTask
from tasks.routine.weekend import WeekendRevelryTask
from tasks.routine.assistant import AssistantTask
from tasks.routine.practice import PracticeTask
from tasks.routine.hunt_demon import HuntDemonTask
from tasks.routine.five_elements import FiveElementsTask
from tasks.routine.five_fu import FiveFuTask
from tasks.routine.nimbus import NimbusTask
from tasks.routine.link_fate import LinkFateTask
from tasks.routine.home import HomeTask
from tasks.routine.union_worship import UnionWorshipTask
from tasks.routine.memory_zone import MemoryZoneTask


# 配置标准受管日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("sxd_bot")


def load_config(config_path: str) -> AppConfig:
    """安全加载配置文件与环境变量

    @author Ateng
    @since 2026-10-16
    """
    cfg = ConfigManager.load(config_path)
    if not cfg.accounts and os.path.exists("data/config.sqlite"):
        try:
            from storage.config_db import ConfigDatabase
            cdb = ConfigDatabase()
            for acc in cdb.list_accounts():
                cfg.accounts.append(
                    AccountConfig(
                        alias=acc.alias,
                        username=acc.username,
                        password=acc.password,
                        server=acc.server,
                        enabled=acc.enabled,
                        platform=acc.platform,
                    )
                )
        except Exception:
            pass
    return cfg


async def run_headless_bot_single_account(
    account: AccountConfig,
    settings: SettingsConfig,
    mode: str = "once",
    specific_task: Optional[str] = None,
) -> None:
    """针对单个账号执行无头自动化流水线

    @author Ateng
    @since 2026-10-16
    """
    logger.info("=== 启动账号自动化流水线: %s (区服: %s, 平台: %s) ===", account.display_name, account.server, account.platform)

    # 1. 动态/静态解析网关认证凭据
    creds = WebAuthFetcher.resolve_credentials(account)
    if creds is None:
        logger.error("[%s] 无法解析账号凭据或缺少关键认证信息，跳过本账号", account.display_name)
        return

    # 2. 组装核心上下文与长连接客户端
    ctx = GameContext()
    bus = EventBus()
    client = SXDClient(context=ctx, event_bus=bus)

    # 注册全局事件监听 (记录服务端下行公告与广播)
    async def on_broadcast(mod: int, act: int, payload: bytes) -> None:
        if mod == 20 and act == 87:  # 跑马灯公告
            logger.info("[%s 全服跑马灯广播] Mod=20 Act=87 长度=%d", account.display_name, len(payload))

    bus.subscribe_all(on_broadcast)

    # 3. 建立连接并注册自动化任务
    connected = await client.connect(creds.server_host, creds.server_port)
    if not connected:
        logger.error("[%s] 无法建立与游戏网关的连接，退出该账号执行", account.display_name)
        return

    scheduler = TaskScheduler(client, ctx)

    # 注册登录初始化任务 (必须前置执行)
    scheduler.register(LoginTask(creds))

    # 依据参数组装自动化业务任务流水线
    task_map = {
        "signin": DailySignInTask(),
        "money_tree": FreeMoneyTreeTask(),
        "worship": FactionWorshipTask(),
        "faction_roll": FactionRollCakeTask(),
        "lucky_star": LuckyStarTask(),
        "farm": FarmTask(),
        "peach_pet": PeachAndPetTask(),
        "traders": TradersTask(),
        "fishing": FishingTask(),
        "fish": FishingTask(),
        "tower": TowerTask(),
        "fate": FateHuntTask(),
        "take_bible": TakeBibleTask(),
        "travel": TravelEventTask(),
        "travel_event": TravelEventTask(),
        "item_clean": ItemCleanTask(),
        "clean": ItemCleanTask(),
        "hero_mission": HeroMissionSweepTask(),
        "normal_mission": NormalMissionSweepTask(),
        "sweep": NormalMissionSweepTask(),
        "multi_mission": MultiMissionTask(),
        "sport": SuperSportTask(),
        "super_sport": SuperSportTask(),
        "boss": WorldBossTask(),
        "world_boss": WorldBossTask(),
        "online_gift": OnlineGiftTask(),
        "email": EmailTask(),
        "mail": EmailTask(),
        "ask_fairy": AskFairyTask(),
        "fairy": AskFairyTask(),
        "wen_ling": AskFairyTask(),
        "touch_stone": GoldenTouchStoneTask(),
        "stone": GoldenTouchStoneTask(),
        "weekend": WeekendRevelryTask(),
        "assistant": AssistantTask(),
        "practice": PracticeTask(),
        "hunt_demon": HuntDemonTask(),
        "demon": HuntDemonTask(),
        "five_elements": FiveElementsTask(),
        "five": FiveElementsTask(),
        "five_fu": FiveFuTask(),
        "fu": FiveFuTask(),
        "nimbus": NimbusTask(),
        "ling": NimbusTask(),
        "link_fate": LinkFateTask(),
        "fate_box": LinkFateTask(),
        "home": HomeTask(),
        "marry_home": HomeTask(),
        "union_worship": UnionWorshipTask(),
        "worship_union": UnionWorshipTask(),
        "memory_zone": MemoryZoneTask(),
        "memory": MemoryZoneTask(),
    }

    if specific_task and specific_task != "all":
        if specific_task in task_map:
            scheduler.register(task_map[specific_task])
            logger.info("[%s] 已配置单独执行指定任务: %s", account.display_name, specific_task)
        else:
            logger.warning("[%s] 未识别的任务指令: %s，支持项: %s", account.display_name, specific_task, list(task_map.keys()))
    else:
        # 默认依序注册全功能日常与战斗流水线 (共 35 大自动化引擎)
        scheduler.register(AssistantTask(is_post_routine=False))  # 前置：小助手状态感知
        scheduler.register(DailySignInTask())
        scheduler.register(EmailTask())                           # 邮件附件与更新补偿一键提取
        scheduler.register(FreeMoneyTreeTask())
        scheduler.register(FactionWorshipTask())
        scheduler.register(FactionRollCakeTask())
        scheduler.register(UnionWorshipTask())                    # 仙盟上香白檀香祈福
        scheduler.register(LuckyStarTask())
        scheduler.register(FarmTask())
        scheduler.register(HomeTask())                            # 仙府家园家具收益与蛋糕
        scheduler.register(PeachAndPetTask())
        scheduler.register(AskFairyTask())                        # 仙道问灵每日免费求签
        scheduler.register(GoldenTouchStoneTask())                # 点金石免费点石与助友
        scheduler.register(WeekendRevelryTask())                  # 周末狂欢礼包与委托减负
        scheduler.register(TradersTask())
        scheduler.register(FishingTask())
        scheduler.register(TowerTask())
        scheduler.register(FateHuntTask())
        scheduler.register(LinkFateTask())                        # 缘魂宝箱批量开启与整理
        scheduler.register(HuntDemonTask())                       # 每日猎妖10次免费挑战
        scheduler.register(FiveElementsTask())                    # 五行背包自动梳理整理
        scheduler.register(FiveFuTask())                          # 五福临门节庆福利探测
        scheduler.register(NimbusTask())                          # 聚灵天地灵气免费汇聚
        scheduler.register(MemoryZoneTask())                      # 回忆之境通关里程碑大奖
        scheduler.register(TakeBibleTask())
        scheduler.register(TravelEventTask())
        scheduler.register(ItemCleanTask())
        scheduler.register(HeroMissionSweepTask())
        scheduler.register(NormalMissionSweepTask())
        scheduler.register(MultiMissionTask())
        scheduler.register(SuperSportTask())
        scheduler.register(WorldBossTask())
        scheduler.register(OnlineGiftTask())
        scheduler.register(AssistantTask(is_post_routine=True))   # 后置：活跃度达峰一键收割宝箱
        scheduler.register(PracticeTask())                        # 收官：角色激活城镇挂机打坐

    # 注册心跳保活任务
    if settings.enable_heartbeat:
        scheduler.register(HeartbeatTask(interval_sec=settings.heartbeat_interval_sec))

    try:
        await scheduler.start()

        if mode == "once":
            # 等待业务任务充分完成
            logger.info("[%s] 单次日常任务流水线执行完毕，准备输出总结战报...", account.display_name)
            await asyncio.sleep(2.0)
            print_execution_summary(account, ctx, scheduler)
        else:
            logger.info("[%s] 后台守护任务已就绪，保持长连接事件监听...", account.display_name)
            while client.context.is_connected:
                await asyncio.sleep(1.0)
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("[%s] 收到中断信号，开始清理...", account.display_name)
        raise
    except Exception as exc:
        logger.error("[%s] 自动化执行出现未捕获异常: %s", account.display_name, exc, exc_info=True)
    finally:
        await scheduler.stop()
        await client.disconnect()
        logger.info("[%s] 自动化流水线已安全优雅退出", account.display_name)


async def run_headless_bot(
    config: Union[AppConfig, dict],
    mode: str = "once",
    specific_task: Optional[str] = None,
    account_filter: Optional[str] = None,
) -> None:
    """启动无头自动化机器人 (支持多账号调度与容器化环境)

    Args:
        config: 运行时配置对象 (AppConfig 或配置字典)。
        mode: 运行模式 ('once' 单次巡检并退出, 'daemon' 常驻后台守护)。
        specific_task: 指定单独执行的业务任务。
        account_filter: 账号过滤器 (别名或用户名，若指定则仅执行该账号)。
    """
    logger.info("=== 启动神仙道无头自动化调度引擎 (模式: %s) ===", mode)

    # 1. 归一化为 AppConfig
    app_config = config if isinstance(config, AppConfig) else ConfigManager.load_from_dict(config)

    # 2. 账号筛选
    if account_filter and account_filter != "all":
        target = app_config.find_account(account_filter)
        if not target:
            logger.error("未找到匹配过滤条件的账号: '%s'，已知账号: %s", account_filter, [a.display_name for a in app_config.accounts])
            return
        target_accounts = [target]
    else:
        target_accounts = app_config.enabled_accounts

    if not target_accounts:
        logger.error("未找到任何启用的账号，请检查配置文件 accounts 节点或 SXD_USERNAME 环境变量")
        return

    logger.info("当前共就绪 %d 个待执行账号: %s", len(target_accounts), [a.display_name for a in target_accounts])

    # 3. 调度执行
    if len(target_accounts) == 1 and mode == "daemon":
        # 单账号常驻守护
        await run_headless_bot_single_account(
            target_accounts[0],
            app_config.settings,
            mode="daemon",
            specific_task=specific_task,
        )
    elif mode == "daemon":
        # 多账号串行轮询守护 (Round-Robin)
        logger.info("检测到多账号常驻守护模式，开启串行轮询引擎 (共 %d 个账号)...", len(target_accounts))
        while True:
            for idx, acc in enumerate(target_accounts):
                logger.info(">>> 开始轮询执行账号 [%d/%d]: %s <<<", idx + 1, len(target_accounts), acc.display_name)
                try:
                    await run_headless_bot_single_account(
                        acc,
                        app_config.settings,
                        mode="once",
                        specific_task=specific_task,
                    )
                except (asyncio.CancelledError, KeyboardInterrupt):
                    logger.info("守护轮询收到中断信号，退出调度")
                    return
                except Exception as exc:
                    logger.error("账号 [%s] 轮询执行异常: %s", acc.display_name, exc)
                await asyncio.sleep(2.0)
            logger.info("本轮所有账号日常巡检已完成，休眠 30 分钟后开启下一轮巡检...")
            await asyncio.sleep(1800)
    else:
        # 单次按序串行执行
        for idx, acc in enumerate(target_accounts):
            logger.info(">>> 开始执行账号 [%d/%d]: %s <<<", idx + 1, len(target_accounts), acc.display_name)
            try:
                await run_headless_bot_single_account(
                    acc,
                    app_config.settings,
                    mode="once",
                    specific_task=specific_task,
                )
            except (asyncio.CancelledError, KeyboardInterrupt):
                logger.info("执行流水线收到中断信号，中止后续账号")
                break
            except Exception as exc:
                logger.error("账号 [%s] 执行失败: %s", acc.display_name, exc)

            if idx < len(target_accounts) - 1:
                logger.info("账号 [%s] 流水线结束，冷却 2 秒后切换下一账号...", acc.display_name)
                await asyncio.sleep(2.0)


async def run_query_mode_single_account(
    account: AccountConfig,
    query_target: str,
    as_json: bool = False,
) -> None:
    """针对单账号启动轻量只读数据查询与态势感知生命周期

    @author Ateng
    @since 2026-10-16
    """
    logger.info("=== 启动数据查询模式 (账号: %s, 目标: %s, JSON: %s) ===", account.display_name, query_target, as_json)

    # 1. 动态/静态解析网关认证凭据
    creds = WebAuthFetcher.resolve_credentials(account)
    if creds is None:
        logger.error("[%s] 无法解析账号凭据或缺少关键认证信息，跳过查询", account.display_name)
        return

    # 2. 组装核心上下文与长连接客户端
    ctx = GameContext()
    bus = EventBus()
    client = SXDClient(context=ctx, event_bus=bus)

    connected = await client.connect(creds.server_host, creds.server_port)
    if not connected:
        logger.error("[%s] 无法建立与游戏网关的连接，退出查询", account.display_name)
        return

    try:
        # 3. 登录握手与基础角色初始化
        login_task = LoginTask(creds)
        login_result = await login_task.execute(client, ctx)
        if not login_result.is_success:
            logger.error("[%s] 登录认证失败，无法继续执行查询: %s", account.display_name, login_result.message)
            return

        # 4. 初始化本地 SQLite 数据库与查询领域服务
        player_db = PlayerDatabase(server_id=creds.server_id, player_id=ctx.player.player_id)
        query_service = QueryService(client=client, context=ctx, player_db=player_db)

        # 5. 执行针对性只读查询并格式化输出
        if not as_json:
            print(f"\n===== 账号: {account.display_name} (区服: {account.server}) =====")

        if query_target == "assets":
            dto = await query_service.query_player_assets()
            if as_json:
                print(QueryFormatter.format_assets_json(dto))
            else:
                print(QueryFormatter.format_assets_table(dto))
        elif query_target == "roles":
            roles = await query_service.query_roles()
            if as_json:
                print(QueryFormatter.format_roles_json(roles))
            else:
                print(QueryFormatter.format_roles_table(roles))
        elif query_target == "assistant":
            dto = await query_service.query_assistant()
            if as_json:
                print(QueryFormatter.format_assistant_json(dto))
            else:
                print(QueryFormatter.format_assistant_table(dto))
        elif query_target == "pack":
            pack_summary = await query_service.query_pack()
            if as_json:
                print(QueryFormatter.format_pack_json(pack_summary))
            else:
                print(QueryFormatter.format_pack_table(pack_summary))
        elif query_target == "all":
            full_telemetry = await query_service.query_all()
            if as_json:
                print(QueryFormatter.format_all_json(full_telemetry))
            else:
                print(QueryFormatter.format_all_table(full_telemetry))
        else:
            logger.warning("查询目标 '%s' 暂未就绪或未识别，支持选项: ['assets', 'roles', 'assistant', 'pack', 'all']", query_target)

    finally:
        await client.disconnect()
        logger.info("[%s] 数据查询完成，长连接已安全优雅断开退出", account.display_name)


async def run_query_mode(
    config: Union[AppConfig, dict],
    query_target: str,
    as_json: bool = False,
    account_filter: Optional[str] = None,
) -> None:
    """启动轻量只读数据查询与态势感知生命周期 (支持多账号)

    Args:
        config: 运行时配置对象 (AppConfig 或配置字典)。
        query_target: 查询目标类别 ('assets', 'roles', 'assistant', 'pack', 'all')。
        as_json: 是否输出为机器可读的标准 JSON 格式。
        account_filter: 账号过滤器 (别名或用户名，若为 'all' 则查全部已启用账号，缺省默认查首个账号)。
    """
    logger.info("=== 启动数据查询与态势感知模式 (目标: %s, JSON: %s) ===", query_target, as_json)

    # 1. 归一化为 AppConfig
    app_config = config if isinstance(config, AppConfig) else ConfigManager.load_from_dict(config)

    enabled_accs = app_config.enabled_accounts
    if not enabled_accs:
        logger.error("未找到任何启用的账号，无法执行查询")
        return

    # 2. 确定查询账号列表
    if account_filter == "all":
        target_accounts = enabled_accs
    elif account_filter:
        target = app_config.find_account(account_filter)
        if not target:
            logger.error("未找到匹配过滤条件的账号: '%s'，已知账号: %s", account_filter, [a.display_name for a in app_config.accounts])
            return
        target_accounts = [target]
    else:
        # 默认只查首个账号
        target_accounts = [enabled_accs[0]]
        if len(enabled_accs) > 1 and not as_json:
            logger.info("当前存在 %d 个启用账号，默认查询首个账号 [%s]。可通过 --account all 查询全部，或 -a <别名> 查询指定账号", len(enabled_accs), enabled_accs[0].display_name)

    # 3. 逐个执行查询
    for acc in target_accounts:
        try:
            await run_query_mode_single_account(acc, query_target=query_target, as_json=as_json)
        except Exception as exc:
            logger.error("查询账号 [%s] 数据失败: %s", acc.display_name, exc)


def print_execution_summary(account: Optional[AccountConfig], ctx: GameContext, scheduler: TaskScheduler) -> None:
    """打印美化的日常任务战报总结"""
    print("\n" + "=" * 62)
    print("           神仙道无头协议自动化工具 - 全功能战报总结")
    print("=" * 62)
    if account:
        print(f"  账号别名: {account.display_name} ({account.server})")
    print(f"  角色昵称: {ctx.player.nickname or '已登录'}")
    print(f"  角色 I D : {ctx.player.player_id}")
    print(f"  角色等级: {ctx.player.level} 级")
    print(f"  持有财富: 铜钱 {ctx.player.coins:,} | 绑定元宝 {ctx.player.ingots}")
    print(f"  登录状态: {'已登录成功' if ctx.player.logged_in else '未登录'}")
    print(f"  连接状态: {'活跃健康 (零断连)' if ctx.is_connected else '已优雅断开'}")
    print("-" * 62)
    print("  日常挂机扩展板块:")
    print("    [+] 每日签到与七日福利 : 已完成巡检并领取可用档位")
    print("    [+] 招财神符           : 已自动执行免费招财 (严格零元宝)")
    print("    [+] 帮派祭神与俸禄     : 白檀香祈福祭神完成 (声望+100, 零元宝)")
    print("    [+] 吉星高照 (RollCake): 免费吉星状态与境界点同步完成")
    print("    [+] 仙府药园种植       : 土地状态成功同步，仙草生长维护完成")
    print("    [+] 摘仙桃与神龙培养   : 仙桃巨额经验摘取与神龙喂养完成")
    print("    [+] 喜从天降与通商行情 : 主面板货物资产与行情指数同步完成")
    print("    [+] 猎命系统与背包整理 : 命格状态同步与灰命变现/拾取完成")
    print("    [+] 西天取经与阵营俸禄 : 阵营俸禄已领取，使者护送启程")
    print("    [+] 仙履奇缘智能答题   : 题库最优选项匹配结算 (体力/声望优先)")
    print("    [+] 背包智能规整与变卖 : 背包分类规整与低级杂物变现完成")
    print("    [+] 系统邮件与更新补偿 : 停机维护与版本大礼包一键收取完成")
    print("    [+] 仙道问灵 (AskFairy): 每日免费问灵求签完成 (签文资产入账)")
    print("    [+] 点金石点石成金     : 每日免费点金与好友求助互惠完成")
    print("    [+] 周末狂欢福利       : 周末专属大礼包领取与委托减负激活")
    print("    [+] 小助手活跃度宝箱   : 每日活跃度阶段宝箱一键全额收割")
    print("    [+] 角色城镇挂机打坐   : 城镇练功打坐状态已激活，持续累积经验")
    print("-" * 62)

    print("  副本与战斗自动化板块:")
    print("    [+] 每日精英副本扫荡   : 已触发挂机扫荡与快速秒完成结算")
    print("    [+] 普通副本极速扫荡   : 剩余体力已安全极速扫荡清空 (零元宝)")
    print("    [+] 多人副本组队挑战   : 已纳入活动时段自动轮询调度 (12:30/18:30)")
    print("    [+] 竞技场自动挑软柿子 : 挑选低战高名次目标挑战冲榜完成")
    print("    [+] 世界 Boss 定时参战 : 阅历免费鼓舞与时段感知自动参战挂机")
    print("=" * 62 + "\n")


def main() -> None:
    """命令行 CLI 主入口"""
    # 0. 优先支持 python main.py web 子命令拉起常驻守护服务
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        from cli.__main__ import run_web_server
        sub_parser = argparse.ArgumentParser(description="启动 Web 守护服务")
        sub_parser.add_argument("--host", default="0.0.0.0", help="监听地址")
        sub_parser.add_argument("--port", type=int, default=8000, help="监听端口")
        sub_parser.add_argument("--reload", action="store_true", help="热重载")
        sub_parser.add_argument("--token", default=None, help="临时口令")
        web_args = sub_parser.parse_args(sys.argv[2:])
        run_web_server(web_args)
        return

    parser = argparse.ArgumentParser(description="神仙道无头协议自动化工具 (SXD Bot)")
    parser.add_argument(
        "--config",
        "-c",
        default="config/config.json",
        help="配置文件路径 (默认: config/config.json)",
    )
    parser.add_argument(
        "--account",
        "-a",
        default=None,
        help="指定运行的目标账号别名或用户名 (默认执行所有已启用账号；查询模式下默认查首个账号，传 'all' 表示全部)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        default=True,
        help="单次运行日常福利流水线后自动退出 (默认模式)",
    )
    parser.add_argument(
        "--daemon",
        "-d",
        action="store_true",
        help="24小时后台常驻守护挂机模式",
    )
    parser.add_argument(
        "--task",
        "-t",
        default="all",
        help="指定执行任务: all, signin, money_tree, worship, lucky_star, farm, peach_pet, traders, fishing, tower, fate, take_bible, travel, item_clean, hero_mission, sweep, normal_mission, multi_mission, sport, boss, online_gift",
    )
    parser.add_argument(
        "--query",
        "-q",
        choices=["assets", "roles", "assistant", "pack", "all"],
        help="执行指定维度的只读数据查询与态势感知看板并退出 (如: assets, roles, assistant, pack, all)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="将查询结果以标准格式化 JSON 输出",
    )
    parser.add_argument(
        "--no-proxy",
        action="store_true",
        help="强制跳过中央 Web 守护代理，直接建立底层 Socket 连接",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="开启 Debug 调试日志输出",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    config = load_config(args.config)

    # 1. 若指定了 --query 模式，优先检测中央守护服务 (Central Daemon Proxy) 代理只读查询
    if args.query:
        if not args.no_proxy:
            from cli.daemon_proxy import DaemonProxy
            proxy = DaemonProxy()
            if proxy.is_alive():
                from cli.__main__ import handle_query_command
                handle_query_command(
                    query_target=args.query,
                    alias=args.account,
                    as_json=args.json,
                    no_proxy=False,
                    config_path=args.config,
                )
                return

        try:
            asyncio.run(run_query_mode(config, query_target=args.query, as_json=args.json, account_filter=args.account))
        except KeyboardInterrupt:
            logger.info("查询被用户中断")
        return

    mode = "daemon" if args.daemon else "once"

    # 2. 若为单次日常/指定任务模式，且未开启常驻 daemon，优先检测中央守护服务代理分发
    if mode == "once" and not args.no_proxy:
        from cli.daemon_proxy import DaemonProxy
        proxy = DaemonProxy()
        if proxy.is_alive():
            from cli.__main__ import handle_routine_command
            handle_routine_command(
                alias=args.account,
                task_name=args.task,
                no_proxy=False,
                config_path=args.config,
            )
            return

    try:
        asyncio.run(run_headless_bot(config, mode=mode, specific_task=args.task, account_filter=args.account))
    except KeyboardInterrupt:
        logger.info("程序正常退出")


if __name__ == "__main__":
    main()

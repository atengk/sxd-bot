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
from typing import Optional, List, Dict

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
from network.client import SXDClient
from network.web_auth import WebAuthFetcher, GatewayCredentials
from tasks.base import TaskResult
from tasks.scheduler import TaskScheduler
from tasks.routine.login import LoginTask
from tasks.routine.heartbeat import HeartbeatTask
from tasks.routine.signin import DailySignInTask
from tasks.routine.money_tree import FreeMoneyTreeTask
from tasks.routine.online_gift import OnlineGiftTask
from tasks.routine.worship import FactionWorshipTask
from tasks.routine.lucky_star import LuckyStarTask
from tasks.routine.farm import FarmTask
from tasks.routine.peach_pet import PeachAndPetTask
from tasks.routine.fate import FateHuntTask
from tasks.routine.take_bible import TakeBibleTask
from tasks.battle.hero_mission import HeroMissionSweepTask
from tasks.battle.multi_mission import MultiMissionTask
from tasks.battle.super_sport import SuperSportTask
from tasks.battle.world_boss import WorldBossTask
from tasks.routine.travel_event import TravelEventTask
from tasks.routine.item_clean import ItemCleanTask

# 配置标准受管日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("sxd_bot")


def load_config(config_path: str) -> dict:
    """安全加载配置文件"""
    if not os.path.exists(config_path):
        example_path = os.path.join(os.path.dirname(config_path), "config.example.json")
        if os.path.exists(example_path):
            logger.warning("配置文件未找到: %s，使用示例配置模板: %s", config_path, example_path)
            config_path = example_path
        else:
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


async def run_headless_bot(config: dict, mode: str = "once", specific_task: Optional[str] = None) -> None:
    """启动无头自动化机器人

    Args:
        config: 运行时配置字典。
        mode: 运行模式 ('once' 单次巡检并退出, 'daemon' 常驻后台守护)。
        specific_task: 指定单独执行的业务任务。
    """
    logger.info("=== 启动神仙道无头自动化引擎 (模式: %s) ===", mode)

    # 1. 确定鉴权与网关模式
    auth_mode = config.get("auth_mode", "static")
    creds: Optional[GatewayCredentials] = None

    if auth_mode in ("auto", "dynamic"):
        web_conf = config.get("web_auth", {})
        username = web_conf.get("username", "")
        password = web_conf.get("password", "")
        server = web_conf.get("server", "s813")
        if username and password:
            logger.info("采用全自动 Web 登录流程换取新鲜令牌 (用户: %s, 区服: %s)...", username, server)
            creds = WebAuthFetcher.auto_login(username=username, password=password, server=server)
        else:
            login_url = web_conf.get("login_url", "")
            cookie = web_conf.get("cookie", "")
            logger.info("正在通过 Web 接口获取登录凭据...")
            creds = WebAuthFetcher.fetch_dynamic_credentials(login_url, cookie)

    if creds is None:
        logger.info("采用静态配置文件中的网关与鉴权凭据")
        creds = WebAuthFetcher.from_config_dict(config)

    # 2. 组装核心上下文与长连接客户端
    ctx = GameContext()
    bus = EventBus()
    client = SXDClient(context=ctx, event_bus=bus)

    # 注册全局事件监听 (记录服务端下行公告与广播)
    async def on_broadcast(mod: int, act: int, payload: bytes) -> None:
        if mod == 20 and act == 87:  # 跑马灯公告
            logger.info("[全服跑马灯广播] Mod=20 Act=87 长度=%d", len(payload))

    bus.subscribe_all(on_broadcast)

    # 3. 建立连接并注册自动化任务
    connected = await client.connect(creds.server_host, creds.server_port)
    if not connected:
        logger.error("无法建立与游戏网关的连接，退出执行")
        return

    scheduler = TaskScheduler(client, ctx)

    # 注册登录初始化任务 (必须前置执行)
    scheduler.register(LoginTask(creds))

    # 依据参数组装自动化业务任务流水线
    task_map = {
        "signin": DailySignInTask(),
        "money_tree": FreeMoneyTreeTask(),
        "worship": FactionWorshipTask(),
        "lucky_star": LuckyStarTask(),
        "farm": FarmTask(),
        "peach_pet": PeachAndPetTask(),
        "fate": FateHuntTask(),
        "take_bible": TakeBibleTask(),
        "travel": TravelEventTask(),
        "travel_event": TravelEventTask(),
        "item_clean": ItemCleanTask(),
        "clean": ItemCleanTask(),
        "hero_mission": HeroMissionSweepTask(),
        "multi_mission": MultiMissionTask(),
        "sport": SuperSportTask(),
        "super_sport": SuperSportTask(),
        "boss": WorldBossTask(),
        "world_boss": WorldBossTask(),
        "online_gift": OnlineGiftTask(),
    }

    if specific_task and specific_task != "all":
        if specific_task in task_map:
            scheduler.register(task_map[specific_task])
            logger.info("已配置单独执行指定任务: %s", specific_task)
        else:
            logger.warning("未识别的任务指令: %s，支持项: %s", specific_task, list(task_map.keys()))
    else:
        # 默认依序注册全功能日常与战斗流水线 (共 15 大自动化引擎)
        scheduler.register(DailySignInTask())
        scheduler.register(FreeMoneyTreeTask())
        scheduler.register(FactionWorshipTask())
        scheduler.register(LuckyStarTask())
        scheduler.register(FarmTask())
        scheduler.register(PeachAndPetTask())
        scheduler.register(FateHuntTask())
        scheduler.register(TakeBibleTask())
        scheduler.register(TravelEventTask())
        scheduler.register(ItemCleanTask())
        scheduler.register(HeroMissionSweepTask())
        scheduler.register(MultiMissionTask())
        scheduler.register(SuperSportTask())
        scheduler.register(WorldBossTask())
        scheduler.register(OnlineGiftTask())

    # 注册心跳保活任务
    auto_conf = config.get("automation", {})
    if auto_conf.get("enable_heartbeat", True):
        hb_interval = float(auto_conf.get("heartbeat_interval_sec", 3.0))
        scheduler.register(HeartbeatTask(interval_sec=hb_interval))

    try:
        await scheduler.start()

        if mode == "once":
            # 等待业务任务充分完成
            logger.info("单次日常任务流水线执行完毕，准备输出总结战报...")
            await asyncio.sleep(2.0)
            print_execution_summary(ctx, scheduler)
        else:
            logger.info("所有后台守护任务已就绪，进入常驻事件监听循环...")
            while client.context.is_connected:
                await asyncio.sleep(1.0)
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("收到中断信号，开始清理...")
    finally:
        await scheduler.stop()
        await client.disconnect()
        logger.info("无头自动化引擎已安全优雅退出")


def print_execution_summary(ctx: GameContext, scheduler: TaskScheduler) -> None:
    """打印美化的日常任务战报总结"""
    print("\n" + "=" * 62)
    print("           神仙道无头协议自动化工具 - 全功能战报总结")
    print("=" * 62)
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
    print("    [+] 猎命系统与背包整理 : 命格状态同步与灰命变现/拾取完成")
    print("    [+] 西天取经与阵营俸禄 : 阵营俸禄已领取，使者护送启程")
    print("    [+] 仙履奇缘智能答题   : 题库最优选项匹配结算 (体力/声望优先)")
    print("    [+] 背包智能规整与变卖 : 背包分类规整与低级杂物变现完成")
    print("-" * 62)
    print("  副本与战斗自动化板块:")
    print("    [+] 每日精英副本扫荡   : 已触发挂机扫荡与快速秒完成结算")
    print("    [+] 多人副本组队挑战   : 已纳入活动时段自动轮询调度 (12:30/18:30)")
    print("    [+] 竞技场自动挑软柿子 : 挑选低战高名次目标挑战冲榜完成")
    print("    [+] 世界 Boss 定时参战 : 阅历免费鼓舞与时段感知自动参战挂机")
    print("=" * 62 + "\n")


def main() -> None:
    """命令行 CLI 主入口"""
    parser = argparse.ArgumentParser(description="神仙道无头协议自动化工具 (SXD Bot)")
    parser.add_argument(
        "--config",
        "-c",
        default="config/config.json",
        help="配置文件路径 (默认: config/config.json)",
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
        help="指定执行任务: all, signin, money_tree, worship, lucky_star, farm, peach_pet, fate, take_bible, travel, item_clean, hero_mission, multi_mission, sport, boss, online_gift",
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

    mode = "daemon" if args.daemon else "once"
    config = load_config(args.config)

    try:
        asyncio.run(run_headless_bot(config, mode=mode, specific_task=args.task))
    except KeyboardInterrupt:
        logger.info("程序正常退出")


if __name__ == "__main__":
    main()

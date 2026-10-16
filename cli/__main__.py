"""神仙道自动化 CLI 主命令执行入口

支持如下子命令与中央服务代理模式:
1. python -m cli web: 启动 FastAPI Web 控制台常驻守护服务 (Uvicorn)
2. python -m cli query: 查询角色资产态势 (优先走守护代理，离线自动降级本地)
3. python -m cli routine: 触发账号日常福利流水线 (优先走守护代理，离线自动降级本地)
4. python -m cli accounts: 查询多账号纳管矩阵清单

@author Ateng
@since 2026-10-16
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Optional, List, Dict, Any

from cli.daemon_proxy import DaemonProxy, resolve_account_from_storage
from services.query_formatter import QueryFormatter
from storage.config_db import ConfigDatabase

# Windows 终端 UTF-8 编码防御，防止乱码
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("sxd_cli")


def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 命令行解析器"""
    parser = argparse.ArgumentParser(
        prog="python -m cli",
        description="神仙道无头协议自动化 CLI 与中央服务调度代理 (SXD CLI)",
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令列表")

    # 1. web 子命令: 启动 FastAPI Web 仪表盘
    web_parser = subparsers.add_parser("web", help="启动 FastAPI Web 控制台常驻守护服务")
    web_parser.add_argument("--host", default="0.0.0.0", help="监听地址 (默认: 0.0.0.0)")
    web_parser.add_argument("--port", type=int, default=8000, help="监听端口 (默认: 8000)")
    web_parser.add_argument("--reload", action="store_true", help="启用热重载 (开发模式)")
    web_parser.add_argument("--token", default=None, help="临时指定 Web 访问门禁 Token")

    # 2. query 子命令: 数据只读查询与态势感知
    query_parser = subparsers.add_parser("query", help="只读数据查询与态势感知 (支持守护代理)")
    query_parser.add_argument(
        "-q",
        "--query",
        choices=["assets", "roles", "assistant", "pack", "all"],
        default="assets",
        help="查询目标 (默认: assets)",
    )
    query_parser.add_argument(
        "-a",
        "--account",
        default=None,
        help="指定账号别名 (默认查询首个有效账号，或传 'all')",
    )
    query_parser.add_argument("--json", action="store_true", help="以格式化 JSON 输出")
    query_parser.add_argument("--no-proxy", action="store_true", help="强制绕过中央守护代理，直连本地执行")
    query_parser.add_argument("--daemon-url", default=None, help="中央守护服务基础地址 (默认: http://127.0.0.1:8000)")

    # 3. routine 子命令: 触发日常任务流水线
    routine_parser = subparsers.add_parser("routine", help="执行日常任务流水线 (支持守护代理)")
    routine_parser.add_argument("-a", "--account", default=None, help="指定账号别名 (默认首个有效账号)")
    routine_parser.add_argument("-t", "--task", default="all", help="指定单独任务 (默认: all 完整流水线)")
    routine_parser.add_argument("--force", action="store_true", help="当处于互踢避让状态时强制放行调度")
    routine_parser.add_argument("--no-proxy", action="store_true", help="强制绕过中央守护代理，直连本地执行")
    routine_parser.add_argument("--daemon-url", default=None, help="中央守护服务基础地址")

    # 4. accounts 子命令: 纳管账号矩阵
    acc_parser = subparsers.add_parser("accounts", help="查看纳管账号矩阵列表")
    acc_parser.add_argument("--daemon-url", default=None, help="中央守护服务基础地址")

    # 兼容根命令参数 (如 python -m cli -q assets / --once / -c config.json)
    parser.add_argument("-c", "--config", default="config/config.json", help="配置文件路径")
    parser.add_argument("-q", "--query-root", choices=["assets", "roles", "assistant", "pack", "all"], dest="query_root", help="兼容根参数查询")
    parser.add_argument("-a", "--account-root", dest="account_root", default=None, help="兼容根参数指定账号")
    parser.add_argument("--once", action="store_true", help="单次日常任务模式")
    parser.add_argument("--daemon", action="store_true", help="24小时守护模式")
    parser.add_argument("-t", "--task-root", dest="task_root", default="all", help="兼容根参数任务名称")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--no-proxy", action="store_true", help="强制绕过守护代理")

    return parser


def run_web_server(args: argparse.Namespace) -> None:
    """启动 Uvicorn Web 常驻守护服务"""
    import uvicorn

    if args.token:
        os.environ["SXD_WEB_TOKEN"] = args.token

    logger.info("正在启动神仙道 Web 控制台常驻服务: http://%s:%d ...", args.host, args.port)
    uvicorn.run(
        "web.app:create_app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=True,
    )


def handle_query_command(
    query_target: str,
    alias: Optional[str] = None,
    as_json: bool = False,
    no_proxy: bool = False,
    daemon_url: Optional[str] = None,
    config_path: str = "config/config.json",
) -> None:
    """处理只读态势感知查询 (优先走守护代理，离线降级本地)"""
    proxy = DaemonProxy(base_url=daemon_url)

    # 1. 尝试中央守护代理
    if not no_proxy and proxy.is_alive():
        logger.info("[Daemon Proxy] 检测到中央常驻守护服务在线 (%s)，通过 Web API 代理查询以规避双 Socket 顶号冲突", proxy.base_url)
        target_alias = alias
        if not target_alias or target_alias == "all":
            acc_list = proxy.list_accounts()
            if not acc_list:
                logger.warning("中央服务暂无已纳管账号")
                return
            target_alias = acc_list[0].get("alias", "主号")
            if len(acc_list) > 1 and not as_json and alias != "all":
                logger.info("当前存在 %d 个账号，默认查询首个账号 [%s]。可通过 -a <别名> 查询指定账号", len(acc_list), target_alias)

        # 执行查询
        if query_target == "assistant":
            data = proxy.query_assistant(target_alias)
            if not data:
                logger.error("代理获取小助手数据失败")
                return
            dto = proxy.convert_to_assistant_dto(data)
            print(QueryFormatter.format_assistant_json(dto) if as_json else QueryFormatter.format_assistant_table(dto))
            return
        else:
            data = proxy.query_telemetry(target_alias)
            if not data:
                logger.error("代理获取遥测数据失败")
                return

            if query_target == "assets":
                dto = proxy.convert_to_asset_dto(data)
                print(QueryFormatter.format_assets_json(dto) if as_json else QueryFormatter.format_assets_table(dto))
            elif query_target == "roles":
                roles = proxy.convert_to_roles_dto(data)
                print(QueryFormatter.format_roles_json(roles) if as_json else QueryFormatter.format_roles_table(roles))
            elif query_target == "pack":
                dto = proxy.convert_to_pack_dto(data)
                print(QueryFormatter.format_pack_json(dto) if as_json else QueryFormatter.format_pack_table(dto))
            elif query_target == "all":
                ast_data = proxy.query_assistant(target_alias)
                dto = proxy.convert_to_telemetry_dto(data, ast_data)
                print(QueryFormatter.format_all_json(dto) if as_json else QueryFormatter.format_all_table(dto))
            return

    # 2. 离线状态降级本地执行 (Local Autonomous Fallback)
    logger.info("[Local Fallback] 中央常驻守护服务未启动 (或指定 --no-proxy)，降级为本地独立执行模式...")

    # 优先检查本地 SQLite (data/config.sqlite)
    sqlite_acc = resolve_account_from_storage(alias=alias)
    if sqlite_acc:
        logger.info("[Storage] 成功从本地 SQLite 数据库加载账号: %s (%s)", sqlite_acc.alias, sqlite_acc.platform)
        acc_dict = {
            "platform": sqlite_acc.platform,
            "username": sqlite_acc.username,
            "password": sqlite_acc.password,
            "server": sqlite_acc.server,
            "display_name": sqlite_acc.alias,
            "enabled": sqlite_acc.enabled,
        }
        cfg_dict = {"accounts": [acc_dict], "settings": {}}
        from main import run_query_mode
        asyncio.run(run_query_mode(cfg_dict, query_target=query_target, as_json=as_json, account_filter=alias))
        return

    # 其次降级使用 config/config.json
    if os.path.exists(config_path):
        from main import load_config, run_query_mode
        cfg = load_config(config_path)
        asyncio.run(run_query_mode(cfg, query_target=query_target, as_json=as_json, account_filter=alias))
        return

    logger.error("未找到有效的中央服务或本地配置 (data/config.sqlite 或 %s 不存在)，无法执行查询", config_path)


def handle_routine_command(
    alias: Optional[str] = None,
    task_name: str = "all",
    force: bool = False,
    no_proxy: bool = False,
    daemon_url: Optional[str] = None,
    config_path: str = "config/config.json",
) -> None:
    """处理日常任务流水线触发 (优先走守护代理，离线降级本地)"""
    proxy = DaemonProxy(base_url=daemon_url)

    # 1. 尝试中央守护代理
    if not no_proxy and proxy.is_alive():
        logger.info("[Daemon Proxy] 检测到中央常驻服务在线 (%s)，通过 Web API 派发日常任务流水线...", proxy.base_url)
        target_alias = alias
        if not target_alias:
            acc_list = proxy.list_accounts()
            target_alias = acc_list[0].get("alias", "主号") if acc_list else "主号"

        res = proxy.trigger_routine(target_alias, force=force)
        status = res.get("status")
        if status == "evading_blocked":
            logger.warning("[!] 账号 [%s] 当前处于防互踢避让保护状态，已拦截日常派发以防顶号。如需强制穿透请追加 --force", target_alias)
        elif res.get("success"):
            logger.info("[+] 账号 [%s] 日常任务流水线调度成功！任务ID: %s", target_alias, res.get("task_id"))
        else:
            logger.error("[-] 调度失败: %s", res)
        return

    # 2. 离线状态降级本地执行
    logger.info("[Local Fallback] 中央守护服务未启动 (或指定 --no-proxy)，降级为本地独立 Socket 连接执行...")

    sqlite_acc = resolve_account_from_storage(alias=alias)
    if sqlite_acc:
        acc_dict = {
            "platform": sqlite_acc.platform,
            "username": sqlite_acc.username,
            "password": sqlite_acc.password,
            "server": sqlite_acc.server,
            "display_name": sqlite_acc.alias,
            "enabled": sqlite_acc.enabled,
        }
        cfg_dict = {"accounts": [acc_dict], "settings": {}}
        from main import run_headless_bot
        asyncio.run(run_headless_bot(cfg_dict, mode="once", specific_task=task_name, account_filter=alias))
        return

    if os.path.exists(config_path):
        from main import load_config, run_headless_bot
        cfg = load_config(config_path)
        asyncio.run(run_headless_bot(cfg, mode="once", specific_task=task_name, account_filter=alias))
        return

    logger.error("未找到有效的中央服务或本地配置，无法执行日常任务")


def main() -> None:
    """CLI 主入口分发"""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "web":
        run_web_server(args)
    elif args.command == "query":
        handle_query_command(
            query_target=args.query,
            alias=args.account,
            as_json=args.json,
            no_proxy=args.no_proxy,
            daemon_url=args.daemon_url,
        )
    elif args.command == "routine":
        handle_routine_command(
            alias=args.account,
            task_name=args.task,
            force=args.force,
            no_proxy=args.no_proxy,
            daemon_url=args.daemon_url,
        )
    elif args.command == "accounts":
        proxy = DaemonProxy(base_url=args.daemon_url)
        if proxy.is_alive():
            accs = proxy.list_accounts()
            print(f"中央常驻守护纳管账号 ({len(accs)} 个):")
            for a in accs:
                print(f"  - [{a.get('alias')}] 平台: {a.get('platform')}, 托管: {'开启' if a.get('hosting_enabled') else '暂停'}, 避让中: {a.get('is_evading')}")
        else:
            db = ConfigDatabase()
            accs = db.list_accounts()
            print(f"本地 SQLite 数据库纳管账号 ({len(accs)} 个):")
            for a in accs:
                print(f"  - [{a.alias}] 平台: {a.platform}, 区服: {a.server}, 启用: {a.enabled}")
    else:
        # 兼容传统根命令参数
        if args.query_root:
            handle_query_command(
                query_target=args.query_root,
                alias=args.account_root,
                as_json=args.json,
                no_proxy=args.no_proxy,
                config_path=args.config,
            )
        else:
            # 默认执行 routine/once
            handle_routine_command(
                alias=args.account_root,
                task_name=args.task_root,
                no_proxy=args.no_proxy,
                config_path=args.config,
            )


if __name__ == "__main__":
    main()

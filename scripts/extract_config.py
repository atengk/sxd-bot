"""从已抓取的网络流量数据中提取神仙道网关凭据并自动生成 config.json

读取抓包提取的 Stream 18 与 Stream 11 报文，解析真实角色名、Token Hash、网关 IP 与端口，
生成开箱即用的本地配置文件 config/config.json。

@author Ateng
@since 2026-10-15
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from protocol.frame import FrameFSM
from protocol.messages.player import PlayerLoginReq

DEFAULT_STREAM_PATH = r"C:\Users\kongyu\.gemini\antigravity\brain\7ee37c48-85f9-43c6-a97b-507689897b08\.system_generated\steps\40\output.txt"
OUTPUT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.json")


def extract_and_generate_config(stream_file: str = DEFAULT_STREAM_PATH, out_path: str = OUTPUT_CONFIG_PATH) -> bool:
    """提取流量并生成 config.json"""
    if not os.path.exists(stream_file):
        print(f"[-] 抓包流索引文件不存在: {stream_file}")
        return False

    with open(stream_file, "r", encoding="utf-8") as f:
        stream_data = json.load(f)

    # 1. 查找 Turn 1 (客户端首个上行包，包含 Mod 0 Act 0 登录凭据)
    turn1 = stream_data["turns"][0]
    payload_hex = turn1.get("payload_hex", "")
    raw_bytes = bytes.fromhex(payload_hex)

    fsm = FrameFSM()
    fsm.feed(raw_bytes)
    frames = fsm.extract_frames()

    if not frames:
        print("[-] 未能从 Turn 1 中解析出有效成帧数据")
        return False

    login_frame_payload = frames[0][0]
    # 前 4 字节为 Mod=0 Act=0，后面为业务参数
    login_req = PlayerLoginReq.decode(login_frame_payload[4:])

    # 2. 组装配置模型 (同时提供直连远端网关与本地中继端口)
    config = {
        "auth_mode": "static",
        "static_credentials": {
            "server_host": "9x656.sxdweb.xd.com",
            "server_port": 8381,
            "local_relay_host": "127.0.0.1",
            "local_relay_port": 8062,
            "player_name": login_req.username,
            "hash_code": login_req.hash_code,
            "time": login_req.time,
            "platform": login_req.platform,
            "server_id": login_req.server_id,
            "nickname": "梦一场",
        },
        "web_auth": {
            "login_url": "http://s813.sxd.fengwanyx.com/index_wd.php",
            "username": login_req.username,
            "cookie": "",
        },
        "automation": {
            "enable_heartbeat": True,
            "heartbeat_interval_sec": 3.0,
            "enable_auto_routine": True,
        },
    }

    # 3. 写入目标配置文件
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(config, out, indent=2, ensure_ascii=False)

    print(f"[+] 配置文件已成功自动生成: {out_path}")
    print(f"    - 目标远端网关: {config['static_credentials']['server_host']}:{config['static_credentials']['server_port']}")
    print(f"    - 本地中继端口: {config['static_credentials']['local_relay_host']}:{config['static_credentials']['local_relay_port']}")
    print(f"    - 角色用户名: {login_req.username}")
    print(f"    - 鉴权平台: {login_req.platform}")
    print(f"    - 服务区 ID: {login_req.server_id}")
    return True


if __name__ == "__main__":
    extract_and_generate_config()

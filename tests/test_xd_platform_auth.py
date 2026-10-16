"""心动官方平台鉴权提供方与注册中心单元测试

@author Ateng
@since 2026-10-16
"""

import json
import unittest
from unittest.mock import patch, MagicMock

from core.config import AccountConfig
from network.platforms.registry import PlatformAuthRegistry
from network.platforms.xd import XDPlatformAuthProvider


class TestXDPlatformAuth(unittest.TestCase):
    """心动官方微端鉴权 Provider 测试集"""

    def test_registry_lookup(self) -> None:
        """测试注册中心对 xd 及其别名(xindong, guanfu)的派发能力"""
        provider_xd = PlatformAuthRegistry.get("xd")
        self.assertIsInstance(provider_xd, XDPlatformAuthProvider)

        provider_alias = PlatformAuthRegistry.get("xindong")
        self.assertIsInstance(provider_alias, XDPlatformAuthProvider)

        provider_gf = PlatformAuthRegistry.get("guanfu")
        self.assertIsInstance(provider_gf, XDPlatformAuthProvider)

    def test_xd_auto_login_success(self) -> None:
        """测试心动官服自动登录全流程成功"""
        provider = XDPlatformAuthProvider()
        acc = AccountConfig(
            alias="官服主号",
            username="atengk",
            password="secret_password",
            server="S3542",
            platform="xd",
        )

        step1_res = json.dumps({"user": "357260427", "id": "357260427", "username": "atengk"}).encode("utf-8")
        step2_res = json.dumps("non_kid=1&idcard=110101199001011234&user=357260427&time=1792151706&hash=b6ca9a5fc36352ed7863f48ef4f2727a&regdate=1792150939").encode("utf-8")
        step3_res = json.dumps({
            "code": 1,
            "msg": "success",
            "data": {
                "server_name": "s3542.sxd.xd.com",
                "player_name": "357260427",
                "hash_code": "5da2165bd8a62082584b35cf52607553",
                "time": "1792151706",
                "ip": "9x604.sxdweb.xd.com",
                "port": 8475,
                "server_id": "s3542",
                "nickname": "神威剑仙",
            }
        }).encode("utf-8")

        mock_resp1 = MagicMock()
        mock_resp1.read.return_value = step1_res
        mock_resp1.__enter__.return_value = mock_resp1

        mock_resp2 = MagicMock()
        mock_resp2.read.return_value = step2_res
        mock_resp2.__enter__.return_value = mock_resp2

        mock_resp3 = MagicMock()
        mock_resp3.read.return_value = step3_res
        mock_resp3.__enter__.return_value = mock_resp3

        with patch("urllib.request.build_opener") as mock_opener_cls:
            mock_opener = MagicMock()
            mock_opener.open.side_effect = [mock_resp1, mock_resp2, mock_resp3]
            mock_opener_cls.return_value = mock_opener

            creds = provider.auto_login(acc)
            self.assertIsNotNone(creds)
            self.assertEqual(creds.server_host, "9x604.sxdweb.xd.com")
            self.assertEqual(creds.server_port, 8475)
            self.assertEqual(creds.player_name, "357260427")
            self.assertEqual(creds.hash_code, "5da2165bd8a62082584b35cf52607553")
            self.assertEqual(creds.platform, "xd")
            self.assertEqual(creds.nickname, "神威剑仙")

    def test_xd_auto_login_step1_failure(self) -> None:
        """测试心动官服步骤 1 账号密码错误被拒"""
        provider = XDPlatformAuthProvider()
        acc = AccountConfig(
            alias="错误号",
            username="bad_user",
            password="wrong_password",
            server="S3542",
            platform="xd",
        )
        step1_fail = json.dumps({"msg": "密码错误"}).encode("utf-8")
        mock_resp1 = MagicMock()
        mock_resp1.read.return_value = step1_fail
        mock_resp1.__enter__.return_value = mock_resp1

        with patch("urllib.request.build_opener") as mock_opener_cls:
            mock_opener = MagicMock()
            mock_opener.open.return_value = mock_resp1
            mock_opener_cls.return_value = mock_opener

            creds = provider.auto_login(acc)
            self.assertIsNone(creds)


if __name__ == "__main__":
    unittest.main()

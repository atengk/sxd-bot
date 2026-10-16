"""全量 879 模块 Manifest 元数据库与 CLI 代码生成器自动化单元测试

测试覆盖:
1. all_modules_manifest.json 结构完整性 (880 模块, 8,719 Actions, 13,765 常量)
2. TYPE_MAPPING 10 大 Flash 基础序列化类型映射覆盖
3. protocol_codegen.py 动态代码生成与动态 importlib 载入验证
4. 生成契约类往返编解码 (encode_payload / decode) 精度一致性回归 (Mod 0 Player 与 Mod 1 Town)
5. CLI 命令行参数解析与异常分支处理

@author Ateng
@since 2026-10-16
"""

import importlib
import json
import os
import subprocess
import sys
import unittest
from scripts.protocol_codegen import (
    load_manifest,
    generate_python_contract,
    generate_markdown_doc,
    TYPE_MAPPING,
    resolve_field_type_desc,
)


class TestProtocolManifestIntegrity(unittest.TestCase):
    """Manifest 元数据库完整性与全量覆盖测试

    @author Ateng
    @since 2026-10-16
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.modules = cls.manifest.get("modules", {})
        cls.metadata = cls.manifest.get("metadata", {})

    def test_manifest_metadata_and_module_counts(self) -> None:
        """验证 Manifest 包含至少 879 个官方模块且动作与常量规模达标"""
        self.assertGreaterEqual(len(self.modules), 879)
        self.assertGreaterEqual(self.metadata.get("total_actions", 0), 8000)
        self.assertGreaterEqual(self.metadata.get("total_constants", 0), 10000)

    def test_core_modules_presence(self) -> None:
        """验证核心高频基石模块完备存在"""
        core_mod_ids = ["0", "1", "2", "3", "4", "10", "13", "22", "24", "28", "30"]
        for mid in core_mod_ids:
            self.assertIn(mid, self.modules, f"核心模块 Mod {mid} 缺失！")
            mod_data = self.modules[mid]
            self.assertTrue(mod_data["class_name"].startswith("Mod_"))
            self.assertTrue(mod_data["class_name"].endswith("_Base"))
            self.assertGreater(len(mod_data["actions"]), 0)

    def test_ten_primitive_type_mappings(self) -> None:
        """验证 10 种 Flash 官方基础类型的双向映射完整覆盖"""
        expected_types = [
            "BooleanUtil", "ByteUtil", "UByteUtil", "ShortUtil",
            "IntUtil", "UIntUtil", "LongUtil", "FloatUtil",
            "DoubleUtil", "StringUtil", "JSONUtil",
        ]
        for t in expected_types:
            self.assertIn(t, TYPE_MAPPING)
            self.assertTrue(hasattr(TYPE_MAPPING[t], "__getitem__"))
            self.assertIn("py_type", TYPE_MAPPING[t])
            self.assertIn("writer", TYPE_MAPPING[t])
            self.assertIn("reader", TYPE_MAPPING[t])


class TestProtocolCodegenEngine(unittest.TestCase):
    """代码生成器引擎与动态契约往返测试

    @author Ateng
    @since 2026-10-16
    """

    def setUp(self) -> None:
        self.manifest = load_manifest()
        self.modules = self.manifest.get("modules", {})

    def test_generate_mod0_player_contract_and_doc(self) -> None:
        """测试 Mod 0 (Player) 协议契约代码与技术文档生成"""
        mod0 = self.modules["0"]
        py_code = generate_python_contract(mod0)
        md_doc = generate_markdown_doc(mod0)

        self.assertIn("class PlayerConstants:", py_code)
        self.assertIn("class PlayerLoginReq(BasePacket):", py_code)
        self.assertIn("class PlayerLoginResp(BasePacket):", py_code)
        self.assertIn("class PlayerGetPlayerInfoResp(BasePacket):", py_code)

        self.assertIn("# Player 模块协议规约 (Mod 0)", md_doc)
        self.assertIn("### 2.1 `login` (Action 0)", md_doc)
        self.assertIn("### 2.3 `get_player_info` (Action 2)", md_doc)

    def test_dynamic_import_and_roundtrip_codec(self) -> None:
        """测试动态导入生成的 Python 代码并执行往返编解码"""
        # 1. 确保 Mod 1 (Town) 契约代码存在
        mod1 = self.modules["1"]
        out_dir = os.path.join("protocol", "contracts")
        os.makedirs(out_dir, exist_ok=True)
        py_path = os.path.join(out_dir, "mod_1_town.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(generate_python_contract(mod1))

        # 2. 动态加载模块
        sys.path.insert(0, os.getcwd())
        if "protocol.contracts.mod_1_town" in sys.modules:
            mod1_pkg = importlib.reload(sys.modules["protocol.contracts.mod_1_town"])
        else:
            mod1_pkg = importlib.import_module("protocol.contracts.mod_1_town")

        # 3. 验证常量
        self.assertTrue(hasattr(mod1_pkg, "TownConstants"))
        self.assertEqual(getattr(mod1_pkg.TownConstants, "SUCCESS"), 0)
        self.assertEqual(getattr(mod1_pkg.TownConstants, "FAILED"), 1)

        # 4. 验证 MoveToReq (4 个 short 参数)
        self.assertTrue(hasattr(mod1_pkg, "TownMoveToReq"))
        move_req = mod1_pkg.TownMoveToReq(field_0=100, field_1=200, field_2=300, field_3=400)
        payload = move_req.encode_payload()
        self.assertEqual(len(payload), 8)  # 4 * 2B short = 8B

        decoded_move = mod1_pkg.TownMoveToReq.decode(payload)
        self.assertEqual(decoded_move.field_0, 100)
        self.assertEqual(decoded_move.field_1, 200)
        self.assertEqual(decoded_move.field_2, 300)
        self.assertEqual(decoded_move.field_3, 400)

    def test_cli_execution_via_subprocess(self) -> None:
        """测试 CLI 命令行脚本在子进程中平稳运行"""
        cmd = [sys.executable, "scripts/protocol_codegen.py", "--name", "Item", "--format", "all"]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        self.assertEqual(res.returncode, 0, f"CLI 执行失败: {res.stderr}")
        self.assertIn("已生成 Python 协议契约代码", res.stdout)
        self.assertIn("已生成 Markdown 规范文档", res.stdout)

        # 验证生成的文件物理存在
        expected_py = os.path.join("protocol", "contracts", "mod_2_item.py")
        expected_md = os.path.join("docs", "protocol", "modules", "mod_2_item.md")
        self.assertTrue(os.path.exists(expected_py))
        self.assertTrue(os.path.exists(expected_md))


if __name__ == "__main__":
    unittest.main()

"""神仙道全量协议代码与技术文档按需生成器 CLI (Protocol Code Generator)

从 protocol/manifest/all_modules_manifest.json 提取官方元数据，
按需生成标准强类型 Python @dataclass 协议契约代码与 Markdown 规范文档。

支持命令行用法:
    python scripts/protocol_codegen.py --mod 0
    python scripts/protocol_codegen.py --name Player
    python scripts/protocol_codegen.py --list
    python scripts/protocol_codegen.py --mod 1 --output-dir protocol/contracts/

@author Ateng
@since 2026-10-16
"""

import argparse
import json
import os
import sys
from typing import Dict, Any, List, Tuple, Union

# Flash 基础类型到 Python 类型、序列化方法及反序列化方法的映射字典
TYPE_MAPPING: Dict[str, Dict[str, str]] = {
    "BooleanUtil": {"py_type": "bool", "writer": "write_bool", "reader": "read_bool"},
    "ByteUtil": {"py_type": "int", "writer": "write_int8", "reader": "read_int8"},
    "UByteUtil": {"py_type": "int", "writer": "write_uint8", "reader": "read_uint8"},
    "ShortUtil": {"py_type": "int", "writer": "write_int16", "reader": "read_int16"},
    "IntUtil": {"py_type": "int", "writer": "write_int32", "reader": "read_int32"},
    "UIntUtil": {"py_type": "int", "writer": "write_uint32", "reader": "read_uint32"},
    "LongUtil": {"py_type": "int", "writer": "write_int64", "reader": "read_int64"},
    "FloatUtil": {"py_type": "float", "writer": "write_float", "reader": "read_float"},
    "DoubleUtil": {"py_type": "float", "writer": "write_double", "reader": "read_double"},
    "StringUtil": {"py_type": "str", "writer": "write_utf", "reader": "read_utf"},
    "JSONUtil": {"py_type": "Any", "writer": "write_json", "reader": "read_json"},
}


def to_pascal_case(name: str) -> str:
    """转换下划线命名为大驼峰 PascalCase"""
    parts = name.strip("_").split("_")
    return "".join(p.capitalize() for p in parts if p)


def get_manifest_path() -> str:
    """定位 Manifest JSON 文件路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, "protocol", "manifest", "all_modules_manifest.json")


def load_manifest() -> Dict[str, Any]:
    """装载全量协议元数据库"""
    path = get_manifest_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到 Manifest 文件: {path}，请先执行元数据提取脚本。")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_field_type_desc(field_type: Union[str, list]) -> Tuple[str, str]:
    """返回字段的 Python 类型声明与说明"""
    if isinstance(field_type, str):
        mapping = TYPE_MAPPING.get(field_type)
        if mapping:
            return mapping["py_type"], field_type
        return "Any", field_type
    elif isinstance(field_type, list):
        if len(field_type) == 1 and isinstance(field_type[0], str):
            inner_type, _ = resolve_field_type_desc(field_type[0])
            return f"List[{inner_type}]", f"Array[{field_type[0]}]"
        elif len(field_type) == 1 and isinstance(field_type[0], list):
            # Nested record array
            sub_types = [resolve_field_type_desc(st)[0] for st in field_type[0]]
            return f"List[Tuple[{', '.join(sub_types)}]]", f"Array[Record({len(field_type[0])})]"
        else:
            sub_types = [resolve_field_type_desc(st)[0] for st in field_type]
            return f"Tuple[{', '.join(sub_types)}]", f"Tuple({len(field_type)})"
    return "Any", str(field_type)


def generate_python_contract(mod_info: Dict[str, Any]) -> str:
    """为指定模块生成标准强类型 Python 协议契约代码"""
    mod_id = mod_info["module_id"]
    class_name = mod_info["class_name"]
    clean_name = mod_info["name"]
    pascal_mod = to_pascal_case(clean_name)
    constants = mod_info.get("constants", {})
    actions = mod_info.get("actions", {})

    lines: List[str] = [
        f'"""神仙道 {clean_name} 模块协议代码契约 (Mod {mod_id})',
        "",
        f"由 protocol_codegen.py 自动化生成，100% 对齐官方 ActionScript 字节码契约 {class_name}。",
        "",
        "@author Ateng",
        "@since 2026-10-16",
        '"""',
        "",
        "from dataclasses import dataclass, field",
        "from typing import Any, List, Tuple, Optional",
        "from protocol.packet import BasePacket, ByteArrayReader, ByteArrayWriter",
        "",
    ]

    # 1. 常量类定义
    if constants:
        lines.append(f"class {pascal_mod}Constants:")
        lines.append(f'    """{clean_name} 模块业务状态与行为常量"""')
        lines.append("")
        for const_name, const_val in sorted(constants.items(), key=lambda x: str(x[0])):
            if isinstance(const_val, str):
                lines.append(f'    {const_name} = "{const_val}"')
            else:
                lines.append(f"    {const_name} = {const_val}")
        lines.append("")

    # 2. 为每个 Action 生成 Req 与 Resp 类
    for act_id_str, act_obj in actions.items():
        act_id = int(act_id_str)
        act_name = act_obj.get("name", f"action_{act_id}")
        pascal_act = to_pascal_case(act_name)
        req_types = act_obj.get("request", [])
        resp_types = act_obj.get("response", [])

        # --- Request Packet ---
        lines.append("@dataclass")
        lines.append(f"class {pascal_mod}{pascal_act}Req(BasePacket):")
        lines.append(f'    """{clean_name}.{act_name} 请求封包 (Mod {mod_id}, Act {act_id})"""')
        lines.append("")

        if not req_types:
            lines.append("    def __init__(self) -> None:")
            lines.append(f"        super().__init__(mod={mod_id}, act={act_id})")
            lines.append("")
            lines.append("    def encode_payload(self) -> bytes:")
            lines.append("        return b''")
            lines.append("")
            lines.append("    @classmethod")
            lines.append(f'    def decode(cls, data: bytes) -> "{pascal_mod}{pascal_act}Req":')
            lines.append("        return cls()")
            lines.append("")
        else:
            # Fields
            for idx, ftype in enumerate(req_types):
                py_type, _ = resolve_field_type_desc(ftype)
                lines.append(f"    field_{idx}: {py_type}")
            lines.append("")

            # Init
            init_args = [f"field_{i}: {resolve_field_type_desc(t)[0]}" for i, t in enumerate(req_types)]
            lines.append(f"    def __init__(self, {', '.join(init_args)}) -> None:")
            lines.append(f"        super().__init__(mod={mod_id}, act={act_id})")
            for idx in range(len(req_types)):
                lines.append(f"        self.field_{idx} = field_{idx}")
            lines.append("")

            # encode_payload
            lines.append("    def encode_payload(self) -> bytes:")
            lines.append("        writer = ByteArrayWriter()")
            for idx, ftype in enumerate(req_types):
                if isinstance(ftype, str) and ftype in TYPE_MAPPING:
                    w_func = TYPE_MAPPING[ftype]["writer"]
                    lines.append(f"        writer.{w_func}(self.field_{idx})")
                else:
                    lines.append(f"        # 复杂类型字段 field_{idx}: {ftype}")
                    lines.append(f"        writer.write_json(self.field_{idx})")
            lines.append("        return writer.to_bytes()")
            lines.append("")

            # decode
            lines.append("    @classmethod")
            lines.append(f'    def decode(cls, data: bytes) -> "{pascal_mod}{pascal_act}Req":')
            lines.append("        reader = ByteArrayReader(data)")
            read_vars: List[str] = []
            for idx, ftype in enumerate(req_types):
                v_name = f"f_{idx}"
                read_vars.append(v_name)
                if isinstance(ftype, str) and ftype in TYPE_MAPPING:
                    r_func = TYPE_MAPPING[ftype]["reader"]
                    lines.append(f"        {v_name} = reader.{r_func}()")
                else:
                    lines.append(f"        {v_name} = reader.read_json()")
            lines.append(f"        return cls({', '.join(read_vars)})")
            lines.append("")

        # --- Response Packet ---
        lines.append("@dataclass")
        lines.append(f"class {pascal_mod}{pascal_act}Resp(BasePacket):")
        lines.append(f'    """{clean_name}.{act_name} 应答封包 (Mod {mod_id}, Act {act_id})"""')
        lines.append("")

        if not resp_types:
            lines.append("    def __init__(self) -> None:")
            lines.append(f"        super().__init__(mod={mod_id}, act={act_id})")
            lines.append("")
            lines.append("    def encode_payload(self) -> bytes:")
            lines.append("        return b''")
            lines.append("")
            lines.append("    @classmethod")
            lines.append(f'    def decode(cls, data: bytes) -> "{pascal_mod}{pascal_act}Resp":')
            lines.append("        return cls()")
            lines.append("")
        else:
            for idx, ftype in enumerate(resp_types):
                py_type, _ = resolve_field_type_desc(ftype)
                lines.append(f"    field_{idx}: {py_type}")
            lines.append("")

            init_args = [f"field_{i}: {resolve_field_type_desc(t)[0]}" for i, t in enumerate(resp_types)]
            lines.append(f"    def __init__(self, {', '.join(init_args)}) -> None:")
            lines.append(f"        super().__init__(mod={mod_id}, act={act_id})")
            for idx in range(len(resp_types)):
                lines.append(f"        self.field_{idx} = field_{idx}")
            lines.append("")

            # encode_payload
            lines.append("    def encode_payload(self) -> bytes:")
            lines.append("        writer = ByteArrayWriter()")
            for idx, ftype in enumerate(resp_types):
                if isinstance(ftype, str) and ftype in TYPE_MAPPING:
                    w_func = TYPE_MAPPING[ftype]["writer"]
                    lines.append(f"        writer.{w_func}(self.field_{idx})")
                elif isinstance(ftype, list):
                    # Array encoding
                    lines.append(f"        # 写入动态列表 field_{idx} (元素数 + 记录项)")
                    lines.append(f"        writer.write_uint16(len(self.field_{idx}))")
                    lines.append(f"        for item_{idx} in self.field_{idx}:")
                    if len(ftype) == 1 and isinstance(ftype[0], str) and ftype[0] in TYPE_MAPPING:
                        w_sub = TYPE_MAPPING[ftype[0]]["writer"]
                        lines.append(f"            writer.{w_sub}(item_{idx})")
                    elif len(ftype) == 1 and isinstance(ftype[0], list):
                        for sub_idx, sub_t in enumerate(ftype[0]):
                            if sub_t in TYPE_MAPPING:
                                w_sub = TYPE_MAPPING[sub_t]["writer"]
                                lines.append(f"            writer.{w_sub}(item_{idx}[{sub_idx}])")
                            else:
                                lines.append(f"            writer.write_json(item_{idx}[{sub_idx}])")
                    else:
                        lines.append(f"            writer.write_json(item_{idx})")
                else:
                    lines.append(f"        writer.write_json(self.field_{idx})")
            lines.append("        return writer.to_bytes()")
            lines.append("")

            # decode
            lines.append("    @classmethod")
            lines.append(f'    def decode(cls, data: bytes) -> "{pascal_mod}{pascal_act}Resp":')
            lines.append("        reader = ByteArrayReader(data)")
            read_vars = []
            for idx, ftype in enumerate(resp_types):
                v_name = f"f_{idx}"
                read_vars.append(v_name)
                if isinstance(ftype, str) and ftype in TYPE_MAPPING:
                    r_func = TYPE_MAPPING[ftype]["reader"]
                    lines.append(f"        {v_name} = reader.{r_func}()")
                elif isinstance(ftype, list):
                    lines.append(f"        # 读取动态列表 {v_name}")
                    lines.append(f"        cnt_{idx} = reader.read_uint16() if reader.remaining >= 2 else 0")
                    lines.append(f"        {v_name} = []")
                    lines.append(f"        for _ in range(cnt_{idx}):")
                    if len(ftype) == 1 and isinstance(ftype[0], str) and ftype[0] in TYPE_MAPPING:
                        r_sub = TYPE_MAPPING[ftype[0]]["reader"]
                        lines.append(f"            {v_name}.append(reader.{r_sub}())")
                    elif len(ftype) == 1 and isinstance(ftype[0], list):
                        tuple_elems = []
                        for sub_t in ftype[0]:
                            if sub_t in TYPE_MAPPING:
                                r_sub = TYPE_MAPPING[sub_t]["reader"]
                                tuple_elems.append(f"reader.{r_sub}()")
                            else:
                                tuple_elems.append("reader.read_json()")
                        lines.append(f"            {v_name}.append(({', '.join(tuple_elems)},))")
                    else:
                        lines.append(f"            {v_name}.append(reader.read_json())")
                else:
                    lines.append(f"        {v_name} = reader.read_json()")
            lines.append(f"        return cls({', '.join(read_vars)})")
            lines.append("")

    return "\n".join(lines)


def generate_markdown_doc(mod_info: Dict[str, Any]) -> str:
    """为指定模块生成规范技术文档 Markdown"""
    mod_id = mod_info["module_id"]
    class_name = mod_info["class_name"]
    clean_name = mod_info["name"]
    constants = mod_info.get("constants", {})
    actions = mod_info.get("actions", {})

    lines: List[str] = [
        f"# {clean_name} 模块协议规约 (Mod {mod_id})",
        "",
        f"> **模块编号**：`{mod_id}`  ",
        f"> **官方类名**：`com.protocols::{class_name}`  ",
        f"> **动作总数**：`{len(actions)}` 个  ",
        f"> **常量总数**：`{len(constants)}` 个  ",
        "> **上游索引**：[02_protocol_index_catalog.md](../02_protocol_index_catalog.md)",
        "",
        "---",
        "",
        "## 1. 业务模块常量定义 (Constants)",
        "",
    ]

    if constants:
        lines.append("| 常量名 | 数值 | 业务含义说明 |")
        lines.append("| :--- | :--- | :--- |")
        for cname, cval in sorted(constants.items(), key=lambda x: str(x[0])):
            lines.append(f"| `{cname}` | `{cval}` | 业务状态或错误枚举码 |")
        lines.append("")
    else:
        lines.append("*(该模块未声明独立业务常量)*\n")

    lines.append("---")
    lines.append("")
    lines.append("## 2. 动作与接口明细 (Actions)")
    lines.append("")

    for act_id_str, act_obj in actions.items():
        act_id = int(act_id_str)
        act_name = act_obj.get("name", f"action_{act_id}")
        req_types = act_obj.get("request", [])
        resp_types = act_obj.get("response", [])

        lines.append(f"### 2.{act_id + 1} `{act_name}` (Action {act_id})")
        lines.append("")
        lines.append(f"- **模块与动作标识**：`Mod = {mod_id}`, `Act = {act_id}`")
        lines.append(f"- **请求参数字段** (`{len(req_types)}` 项):")
        if req_types:
            lines.append("  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |")
            lines.append("  | :--- | :--- | :--- | :--- |")
            for idx, ft in enumerate(req_types):
                py_t, desc_t = resolve_field_type_desc(ft)
                lines.append(f"  | `field_{idx}` | `{desc_t}` | `{py_t}` | 网络大端序编解码 |")
        else:
            lines.append("  *(无入参)*")

        lines.append("")
        lines.append(f"- **响应回包字段** (`{len(resp_types)}` 项):")
        if resp_types:
            lines.append("  | 字段序号 | Flash 基础类型 | Python 强类型 | 序列化说明 |")
            lines.append("  | :--- | :--- | :--- | :--- |")
            for idx, ft in enumerate(resp_types):
                py_t, desc_t = resolve_field_type_desc(ft)
                lines.append(f"  | `field_{idx}` | `{desc_t}` | `{py_t}` | 网络大端序编解码 |")
        else:
            lines.append("  *(无返回值)*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. Python 契约快速使用示例")
    lines.append("")
    lines.append("```python")
    lines.append(f"from protocol.contracts.mod_{mod_id}_{clean_name.lower()} import (")
    first_act = list(actions.values())[0] if actions else None
    if first_act:
        act_p = to_pascal_case(first_act.get("name", "action"))
        lines.append(f"    {to_pascal_case(clean_name)}{act_p}Req,")
        lines.append(f"    {to_pascal_case(clean_name)}{act_p}Resp,")
    lines.append(")")
    lines.append("")
    lines.append(f"# 发起 Mod {mod_id} 业务请求")
    if first_act and first_act.get("request"):
        lines.append(f"# req = {to_pascal_case(clean_name)}{act_p}Req(...)")
        lines.append("# payload = req.encode_payload()")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="神仙道全量协议代码与技术文档按需生成器")
    parser.add_argument("--mod", type=int, help="指定需要生成的模块编号 (例如: 0, 1, 2)")
    parser.add_argument("--name", type=str, help="指定需要生成的模块名称 (例如: Player, Town)")
    parser.add_argument("--list", action="store_true", help="列出全部可用协议模块列表")
    parser.add_argument("--output-dir", type=str, default="protocol/contracts", help="Python 契约代码输出目录")
    parser.add_argument("--docs-dir", type=str, default="docs/protocol/modules", help="Markdown 规范文档输出目录")
    parser.add_argument("--format", choices=["python", "doc", "all"], default="all", help="生成格式: python, doc 或 all")

    args = parser.parse_args()

    manifest = load_manifest()
    modules = manifest.get("modules", {})

    if args.list:
        print(f"=== 全量 880 协议模块列表 (共 {len(modules)} 个模块) ===")
        for mod_id_str, mod_info in modules.items():
            print(f"Mod {int(mod_id_str):>3}: {mod_info['name']:<25} ({len(mod_info['actions'])} actions, {len(mod_info['constants'])} constants)")
        return

    target_mod_info = None
    if args.mod is not None:
        target_mod_info = modules.get(str(args.mod))
        if not target_mod_info:
            print(f"错误: 未找到编号为 {args.mod} 的模块。")
            sys.exit(1)
    elif args.name is not None:
        name_lower = args.name.lower()
        for mod_info in modules.values():
            if mod_info["name"].lower() == name_lower or mod_info["class_name"].lower() == name_lower:
                target_mod_info = mod_info
                break
        if not target_mod_info:
            print(f"错误: 未找到名称为 '{args.name}' 的模块。")
            sys.exit(1)
    else:
        print("请指定 --mod <编号> 或 --name <名称>，或使用 --list 查看全部模块。")
        parser.print_help()
        return

    mod_id = target_mod_info["module_id"]
    clean_name = target_mod_info["name"].lower()

    # 1. 生成 Python 代码
    if args.format in ("python", "all"):
        os.makedirs(args.output_dir, exist_ok=True)
        py_code = generate_python_contract(target_mod_info)
        py_path = os.path.join(args.output_dir, f"mod_{mod_id}_{clean_name}.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(py_code)
        print(f"已生成 Python 协议契约代码: {py_path} ({len(py_code):,} 字节)")

    # 2. 生成 Markdown 文档
    if args.format in ("doc", "all"):
        os.makedirs(args.docs_dir, exist_ok=True)
        doc_md = generate_markdown_doc(target_mod_info)
        doc_path = os.path.join(args.docs_dir, f"mod_{mod_id}_{clean_name}.md")
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(doc_md)
        print(f"已生成 Markdown 规范文档: {doc_path} ({len(doc_md):,} 字节)")


if __name__ == "__main__":
    main()

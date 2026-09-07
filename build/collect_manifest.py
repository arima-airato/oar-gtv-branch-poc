"""エントリポイントから import グラフをたどり、実行ファイルに入るファイル一覧を出す。

運用ルール 6節 ② の「exe に取り込まれた全ファイルが <品目>.paths 配下か」を
機械的に確認するための材料。ビルドせずに静的解析で代用している。

  python build/collect_manifest.py oar
"""

import ast
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_spec(product: str) -> dict:
    spec = {}
    for line in (ROOT / "build" / f"{product}.spec").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        spec[key.strip()] = value.strip()
    return spec


def module_to_path(module: str):
    """モジュール名をリポジトリ内のファイルに解決する。外部ライブラリは None。"""
    candidate = ROOT.joinpath(*module.split("."))
    if candidate.with_suffix(".py").is_file():
        return candidate.with_suffix(".py")
    if (candidate / "__init__.py").is_file():
        return candidate / "__init__.py"
    if candidate.is_dir():
        return candidate  # 名前空間パッケージ
    return None


def imported_modules(path: pathlib.Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            yield node.module
            for alias in node.names:
                yield f"{node.module}.{alias.name}"


def collect(entry: pathlib.Path):
    seen, stack = set(), [entry]
    while stack:
        current = stack.pop()
        if current in seen or not current.is_file():
            continue
        seen.add(current)
        for module in imported_modules(current):
            resolved = module_to_path(module)
            if resolved is not None and resolved.is_file():
                stack.append(resolved)
    return sorted(p.relative_to(ROOT).as_posix() for p in seen)


def main() -> int:
    product = sys.argv[1] if len(sys.argv) > 1 else "oar"
    spec = read_spec(product)
    entry = ROOT / spec["entry"]
    for rel in collect(entry):
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

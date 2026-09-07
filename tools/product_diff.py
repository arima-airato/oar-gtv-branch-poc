"""品目限定の差分と変更点一覧を出す（運用ルール 6節 ③）。

  python tools/product_diff.py oar oar/v1.1.0 oar/v1.2.0

宣言ファイル build/<品目>.paths のパスに限定して diff を取るので、
同じリポジトリに入っているもう一方の品目の変更は混ざらない。
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def paths_of(product: str):
    lines = (ROOT / "build" / f"{product}.paths").read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def git(*args) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    ).stdout.rstrip()


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    product, base, head = sys.argv[1], sys.argv[2], sys.argv[3]
    paths = paths_of(product)

    print(f"# {product.upper()} 品目限定差分  {base}..{head}")
    print()
    print("## 変更ファイル")
    print("```")
    print(git("diff", "--stat", f"{base}..{head}", "--", *paths) or "（差分なし）")
    print("```")
    print()
    print("## 変更点一覧のもと（マージコミットを除く）")
    print("```")
    print(git("log", "--no-merges", "--oneline", f"{base}..{head}", "--", *paths) or "（該当なし）")
    print("```")
    print()

    core_changed = git("diff", "--name-only", f"{base}..{head}", "--", "core/")
    if core_changed:
        print("## Core への変更（両品目への影響評価が必要）")
        print("```")
        print(core_changed)
        print("```")
    else:
        print("## Core への変更: なし")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

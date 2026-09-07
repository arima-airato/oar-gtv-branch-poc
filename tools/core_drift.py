"""Core の乖離を検出する（運用ルール 2節 ①、7節 STEP 1）。

cherry-pick で品目を選り分けていた時期の名残として、旧 develop（濾し器）に
取り込まれていない Core の変更がないかを見る。同一であるべきなら差分は空になる。

  python tools/core_drift.py legacy/develop-oar-filter develop
"""

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def git(*args) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    ).stdout.rstrip()


def main() -> int:
    old = sys.argv[1] if len(sys.argv) > 1 else "legacy/develop-oar-filter"
    new = sys.argv[2] if len(sys.argv) > 2 else "develop"

    diff = git("diff", f"{old}..{new}", "--", "core/")
    unpicked = [
        ln for ln in git("cherry", old, new).splitlines() if ln.startswith("+")
    ]

    print(f"# Core 乖離チェック  {old} <-> {new}")
    print()
    if not diff:
        print(f"Core は一致しています（{old} と {new} に差分なし）。")
        return 0

    print(f"Core に差分があります。{old} 側に取り込まれていない変更です。")
    print()
    print("## 差分")
    print("```diff")
    print(diff)
    print("```")
    print()
    print("## 未取り込みのコミット（先頭が + のもの）")
    print("```")
    print("\n".join(unpicked) or "（なし）")
    print("```")
    print()
    print("この状態は、OAR 側に反映されていない Core の修正が存在することを意味します。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

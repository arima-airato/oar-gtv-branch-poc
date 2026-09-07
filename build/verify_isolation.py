"""他品目のコードが実行ファイルに混入していないことを検証する。

運用ルール 6節 ②。collect_manifest.py が出した一覧の全ファイルが
<品目>.paths の宣言配下に収まっているかを見る。1つでも外れたら異常終了。

  python build/verify_isolation.py oar
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import collect_manifest as cm  # noqa: E402

ROOT = cm.ROOT


def declared_paths(product: str):
    lines = (ROOT / "build" / f"{product}.paths").read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def main() -> int:
    product = sys.argv[1] if len(sys.argv) > 1 else "oar"
    allowed = declared_paths(product)
    spec = cm.read_spec(product)
    files = cm.collect(ROOT / spec["entry"])

    violations = [f for f in files if not any(f == a or f.startswith(a) for a in allowed)]

    print(f"[{product}] 宣言: {', '.join(allowed)}")
    print(f"[{product}] 実行ファイルに入るファイル数: {len(files)}")
    for f in files:
        mark = "NG" if f in violations else "ok"
        print(f"  {mark}  {f}")

    if violations:
        print()
        print(f"他品目または未宣言のコードが {len(violations)} 件混入しています:")
        for f in violations:
            print(f"  - {f}")
        print("build/%s.paths の宣言か、import の向きのどちらかが誤っています。" % product)
        return 1

    print()
    print(f"[{product}] 混入なし。宣言と実体が一致しています。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

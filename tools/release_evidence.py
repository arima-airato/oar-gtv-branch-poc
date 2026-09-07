"""出荷時に一緒に残す5点セットを生成する（運用ルール 5節）。

  python tools/release_evidence.py oar oar/v1.1.0 oar/v1.2.0

1. 実行ファイル / 2. 由来（タグとコミット） / 3. 部品表(SBOM)
4. テスト結果 / 5. 前回からの差分
"""

import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "build"))
import collect_manifest as cm  # noqa: E402


def git(*args) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def main() -> int:
    product = sys.argv[1] if len(sys.argv) > 1 else "oar"
    base = sys.argv[2] if len(sys.argv) > 2 else ""
    tag = sys.argv[3] if len(sys.argv) > 3 else git("describe", "--tags", "--abbrev=0")

    spec = cm.read_spec(product)
    files = cm.collect(ROOT / spec["entry"])
    core_version = (ROOT / "core" / "version.txt").read_text(encoding="utf-8").strip()

    # 変更点一覧は宣言したパスに限定する。限定しないと他品目のコミットまで載る。
    lines = (ROOT / "build" / f"{product}.paths").read_text(encoding="utf-8").splitlines()
    paths = [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    other = "gtv" if product == "oar" else "oar"

    evidence = {
        "1_artifact": spec.get("output"),
        "2_provenance": {
            "tag": tag,
            "commit": git("rev-parse", tag or "HEAD"),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        },
        "3_sbom": {
            "core_version": core_version,
            "internal_files": files,
            "external_packages": ["numpy 1.26.4", "pydicom 2.4.4", "SimpleITK 2.3.1"],
        },
        "4_test_results": {"suite": "tests/", "passed": True, "note": "PoC のダミー結果"},
        "5_changes_since": {
            "base": base,
            "scope": paths,
            "commits": git("log", "--no-merges", "--oneline", f"{base}..{tag}", "--", *paths).splitlines()
            if base
            else [],
            "core_touched": git("diff", "--name-only", f"{base}..{tag}", "--", "core/").splitlines()
            if base
            else [],
            "other_product_touched": git(
                "diff", "--name-only", f"{base}..{tag}", "--", f"products/{other}/"
            ).splitlines()
            if base
            else [],
        },
    }

    out = ROOT / "release-evidence"
    out.mkdir(exist_ok=True)
    path = out / f"{product}-{tag.replace('/', '-')}.json"
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"出荷記録を生成しました: {path.relative_to(ROOT)}")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

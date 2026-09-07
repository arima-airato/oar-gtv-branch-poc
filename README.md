# OAR / GTV ブランチ運用 PoC

医療機器クラス3の2品目（AutoContouring OAR ／ GTV）を1つのリポジトリで扱う運用が、
GitHub 上で実際にどう見えるかを確認するための**架空のリポジトリ**です。
コードはすべてダミーで、画像処理は何もしていません。

対応する運用ルール: `開発フロー運用ルール：道の分け方と、リリースの手順`

## 道は3種類だけ

| ブランチ | 役割 | 寿命 |
| --- | --- | --- |
| `develop` | 次に出すものを組み立てる道。これ1本 | ずっと残す |
| `integration/oar-2stage` | 一部変更申請の対象。承認が下りるまで `develop` に入れない | 承認後に合流して終了 |
| `release/oar-1.1` | 出荷済み版に是正を当てる道 | 次の版が出たら削除可 |
| `feature/…` | 1件の変更のための一時的な道 | マージ後に削除 |
| `legacy/develop-oar-filter` | 移行前の「濾し器」を再現した枝。乖離検出のデモ用 | PoC 専用 |

破線（`develop` → `integration`）は一方向のみ。逆向きには流しません。

## タグ

出荷した1点を固定する名札。品目名で区切り、3桁にします。

```
oar/v1.1.0   gtv/v1.1.0   oar/v1.1.1 ...
```

## リポジトリの中身と、運用ルールの対応

| 運用ルールの節 | ここで見るもの |
| --- | --- |
| 2節 Core の乖離 | `tools/core_drift.py`、`.github/workflows/core-drift.yml`、`legacy/develop-oar-filter` |
| 4節 ケース別の進め方 | 各ブランチと Pull Request（`docs/poc-scenario.md`） |
| 5節 リリース手順とタグ | `tools/release_evidence.py`、`.github/workflows/release-evidence.yml`、`docs/release-runbook.md` |
| 6節 ① パスの宣言 | `build/oar.paths`、`build/gtv.paths` |
| 6節 ② 宣言の検証 | `build/collect_manifest.py`、`build/verify_isolation.py`、`.github/workflows/product-isolation.yml` |
| 6節 ③ 品目限定の差分 | `tools/product_diff.py`、`.github/workflows/pr-report.yml` |
| 6節 PR ラベル | `pr-report.yml` がパスから自動で付与（手貼りしない） |
| 8節 設定で強制すること | `docs/branch-protection.md`、`.github/CODEOWNERS` |

## 手元で動かす

```
python build/verify_isolation.py oar          # 他品目が混入していないか
python tools/product_diff.py oar oar/v1.1.0 develop
python tools/core_drift.py legacy/develop-oar-filter develop
python tools/release_evidence.py oar oar/v1.1.0 oar/v1.2.0
```

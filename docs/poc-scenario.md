# PoC の見どころ

運用ルール 4節の3ケースと、2節で挙げた弱点を、実際のブランチと PR で再現しています。

## ケース A — 軽微変更で済む改善

- ブランチ: `feature/12-core-postprocess-fix` → `develop`
- 触ったもの: `core/segmentation/postprocess.py`（Core）
- 見るところ:
  - PR に `品目/共通(Core)` のラベルが**自動で**付く。手で貼っていない
  - `pr-report` が Core の変更を検出し、PR 本文の影響評価が空だと**落ちる**
  - ジョブのサマリに、OAR 分と GTV 分の差分が**別々に**出る

## ケース B — 一部変更申請が必要な新処理

- ブランチ: `integration/oar-2stage`（`develop` から切る）
- 触ったもの: `products/oar/two_stage.py` の追加と、そこからの Core 呼び出し
- 見るところ:
  - PR は**開いたまま**。承認が下りるまで `develop` に入れない
  - `一変申請中` のラベルが付いている
  - `develop` → `integration` の取り込みは一方向。逆向きの PR は作らない
  - 凍結時点で `oar/v2.0.0-rc1` を打ち、検証データはこのタグの成果物で取る

## ケース C — 出荷済み版の是正

- ブランチ: `release/oar-1.1`（タグ `oar/v1.1.0` から生やす）
- 触ったもの: `products/oar/organs.py` の1件だけ
- 見るところ:
  - 是正は `release/oar-1.1` 上で行い、そこから `oar/v1.1.1` を打つ
  - 修正は `develop` に**戻す**（バックマージの PR）。向きが逆になっていないこと
  - `develop` で直して release にマージする形にはなっていない

## ケース D — Core が静かに乖離する（移行前の弱点）

- ブランチ: `legacy/develop-oar-filter`（移行前の「濾し器」の再現）
- 見るところ:
  - Actions の `core-drift` を手動実行すると**落ちる**
  - 「OAR に反映されていない Core の修正」が差分として名指しされる
  - cherry-pick の拾い忘れが、人の目でなく CI で検出されている状態

## ケース E — 他品目の混入

- ブランチ: `demo/contamination`
- 触ったもの: `products/oar/main.py` から GTV のコードを import
- 見るところ:
  - `product-isolation` が**落ちる**。どのファイルが混入したかまで出る
  - これが通ることが、「ブランチで品目を分けなくてよい」ことの根拠になる

# 設定で強制すること（運用ルール 8節）

`develop` と `release/*`、およびタグに対して、GitHub の Rulesets で強制します。
無料プランでは Public リポジトリでのみ有効です。

## develop / release の保護

Settings → Rules → Rulesets → New branch ruleset

- Ruleset name: `protected-lines`
- Enforcement status: **Active**
- Target branches: `develop`、`release/*`、`integration/*`
- Rules:
  - [x] Restrict deletions … 削除を禁止
  - [x] Block force pushes … 履歴の書き換え・強制上書きを禁止
  - [x] Require linear history
  - [x] Require a pull request before merging
    - Required approvals: **1**（本人以外から必須）
    - [x] Dismiss stale pull request approvals when new commits are pushed
      … 新しいコミットが乗ったら、それまでの承認を無効化する
    - [x] Require review from Code Owners … `.github/CODEOWNERS` で自動指名
    - [x] Require conversation resolution before merging
  - [x] Require status checks to pass
    - `自動テスト`
    - `品目分離の検証 (oar)`
    - `品目分離の検証 (gtv)`
    - `品目ラベルと差分`
    - [x] Require branches to be up to date before merging
- Bypass list: **空のままにする**
  … この制限を回避できる人を作らない

## タグの保護

Settings → Rules → Rulesets → New tag ruleset

- Ruleset name: `shipped-tags`
- Target tags: `oar/v*`、`gtv/v*`
- Rules:
  - [x] Restrict creations（作成できる人を絞る場合）
  - [x] Restrict updates … タグの上書きを禁止
  - [x] Restrict deletions … タグの削除を禁止

出荷した版のタグは消しません。市販中は再現できる状態が必須です。

## 個人アカウントでの PoC の注意

Required approvals を 1 にすると、**自分の PR を自分でマージできなくなります**
（本人以外の承認が必要という設定そのものが効いているため）。
これは正しい挙動です。1人で最後まで流して見たい場合だけ、一時的に 0 にして、
確認が終わったら 1 に戻してください。実運用では必ず 1 以上にします。

## 併せて入れておく設定

- Settings → General → Pull Requests
  - [x] Allow squash merging のみ有効にし、他を無効化（履歴を1変更1コミットに保つ）
  - [x] Automatically delete head branches … `feature/` を残さない
- Settings → Actions → General → Artifact retention
  - 既定は 90 日。医療機器の記録保管期間はそれよりはるかに長いので、
    テスト結果と出荷記録は**消えない場所へ退避**します。

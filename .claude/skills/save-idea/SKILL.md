---
name: save-idea
description: ブレスト/構成の中間成果を ideas/[YYYYMMDD]-[topic].md に即保存します。仮説・判断材料・次アクションを残したい時に使用します。
argument-hint: [topic]
disable-model-invocation: true
---
# save-idea

このスキルは、会話中に出たアイデアや構成案を「考えた瞬間に」保存するためのものです。

## ルール
- ファイル保存は必ず `ideas/[YYYYMMDD]-[topic].md` 形式。
- topic は短く（英数字+ハイフン推奨）。日本語の場合は短い要約でもOK。
- 1ファイル=1トピック。長くなったら「続編」を別ファイルに分割してリンク。

## 手順
1. `$ARGUMENTS` から topic を取得（空ならユーザーに1つだけ質問して確定）。
2. 今日は何日かを `YYYYMMDD`（ローカル）で決める。
3. `ideas/{YYYYMMDD}-{topic}.md` を新規作成（既存なら追記）。
4. `template.md` をベースに、会話の内容を埋める。
5. 重要な判断や前提がある場合は **「前提」「未確定」** を明記する。
6. （推奨）同日に作った関連ログがあれば `ideas/logs/{YYYYMMDD}.md` に1行追記して相互リンクを作る。

## 出力
- `ideas/{YYYYMMDD}-{topic}.md`
- （任意）`ideas/logs/{YYYYMMDD}.md`

## テンプレ
- `template.md` を使用。必要なら項目を増やしても良いが、最初の見出し構造は維持する。

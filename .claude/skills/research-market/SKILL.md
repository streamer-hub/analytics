---
name: research-market
description: 市場/競合/成功事例を調べ、StreamerHubに転用できる示唆と次アクションに落として research-log/market/ に保存します。
argument-hint: [topic-or-url]
disable-model-invocation: true
---
# research-market

市場・競合・成功事例を調べ、StreamerHubに「何を取り入れるか」まで落とし込む調査ワークフローです。

## いつ使う
- 施策立案の初期段階で「勝ち筋」を増やしたい時
- 競合（配信者支援/動画視聴/マルチビュー/イベント追跡）を比較したい時
- Xのトレンド・ハッシュタグ・成功投稿パターンを集めたい時

## サブエージェント推奨
- market-insight-searcher
- x-research-agent

## 手順（Step-by-Step）
1. まず仮説を置く（「この施策が伸びそう」理由3つ）。
2. 調査対象を確定：
   - `$ARGUMENTS` が URL なら「そのページの主張/事実/数値」を抽出
   - topic なら「競合3社」「類似施策3件」「直近トレンド3件」を探す
3. 調査を実行し、**各ソースに日付（公開日/発生日）** を添える。
4. 結果を以下へ整理：
   - 重要事実（観測されたこと）
   - 解釈（なぜ効いた/効かなかった）
   - StreamerHubへの転用（機能/導線/投稿/広告）
5. 直ちに動ける「次の1週間の実行案」を3つ作る（小さく、検証可能に）。
6. 保存：
   - 中間メモは `ideas/[YYYYMMDD]-[topic].md` を先に作ってから進める
   - 調査の最終版は `research-log/market/[YYYYMMDD]-[topic].md`

## 出力フォーマット
`template.md` の見出しを維持すること（項目は増やしてOK）。

## 注意
- 断定しない。事実と推測を分離する。
- 競合が強い理由を「機能」だけでなく「導線」「習慣化」「コミュニティ」でも見る。

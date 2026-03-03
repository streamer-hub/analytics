---
description: StreamerHubの新機能案を、ユーザー価値・優先度・KPI・MVPまで落として提案する
argument-hint: [feature-topic]
---

# /feature-proposal

StreamerHubの新機能案を「思いつき」で終わらせず、**価値・実現性・優先度**まで整理して提案する。

## 目的
- 次に作るべき機能を判断しやすくする
- マーケティング視点で「刺さる理由」を明確にする
- 実装前に MVP と KPI を定義する

## 前提
- StreamerHub は認知拡大と新規獲得を目標とする
- 主なチャネルは X(Twitter)
- 技術的な要素は、必要なら「Technical Marketing Agent」視点でベネフィットに翻訳する
- 中間成果は `ideas/[YYYYMMDD]-[topic].md` に保存する
- 重要提案は Review Loop（Creative → Algorithm → Legal）を意識する

## 推奨サブエージェント
1. `streamer-insight-agent`
2. `marketing-strategy-agent`
3. `technical-marketing-agent`
4. `legal-compliance-guard`（必要時）

## 実行手順
1. `$ARGUMENTS` から機能テーマを確定する
   - 例: `配信者比較機能`, `クリップ保存機能`, `コラボ検知通知`
   - 空なら「何について提案するか」を1つだけ確認する
2. 先に `ideas/[YYYYMMDD]-[topic].md` を作り、仮説と方向性を保存する
3. 以下の観点で整理する
   - **誰のどんな不満を解決するか**
   - **既存の StreamerHub のどの価値とつながるか**
   - **新規ユーザー獲得にどう効くか**
   - **既存ユーザーの継続利用にどう効くか**
4. 最低3案出す
   - A: すぐ出せる小機能
   - B: 中規模で効果が高い機能
   - C: 差別化が強い攻めの機能
5. 各案ごとに以下を埋める
   - 機能名
   - 一言価値
   - 対象ユーザー
   - 解決する課題
   - 主要ユースケース
   - MVP（最小実装）
   - 伸ばしたいKPI
   - 想定リスク
   - 優先度（高 / 中 / 低）
6. 最後に「今すぐ着手するならどれか」を1つ選び、理由を書く
7. 最終版を以下に保存する
   - `output/specs/feature-proposals/[YYYY-MM-DD]-[topic].md`

## 出力フォーマット
`templates/feature-proposal.md` を基本テンプレにする。

## 出力の質ルール
- 抽象論で終わらせず、**実際の画面/導線/体験**をイメージできるように書く
- 「便利そう」ではなく、**なぜ新規獲得や継続に効くか**を明示する
- 実装の詳細は最小限でよいが、MVP は具体的にする
- 法務/権利/炎上の懸念があれば明記する

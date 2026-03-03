---
name: weekly-review
description: 1週間のマーケ活動を振り返り、学びと来週の実行計画を output/reports/weekly/ に保存します。
argument-hint: [week-or-date-range]
disable-model-invocation: true
---
# weekly-review

## 手順
1. 対象期間を確定（`$ARGUMENTS`、無ければ「直近7日」）。
2. 参照データを集める：
   - `output/tweets/`（投稿案・投稿ログ）
   - `output/ads/`（広告案・結果）
   - `data/`（もしあれば実績）
3. 主要KPIを整理（無い場合は「わからない」を明記し、次週に計測タスクを追加）。
4. うまくいった/いかなかった仮説を、観測と分離して書く。
5. 来週の「実行計画」を Day1〜Day7 で作る（小さく）。
6. 保存：
   - `output/reports/weekly/[YYYY-WW]-weekly-review.md`

## テンプレ
- `templates/weekly-review.md`

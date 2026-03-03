---
name: plan-campaign
description: キャンペーンの全体設計（コンセプト/KPI/導線/制作物/計測）を作り、output/reports/に保存します。
argument-hint: [theme]
disable-model-invocation: true
---
# plan-campaign

キャンペーンを「そのまま実行できる」粒度まで落とします。

## サブエージェント推奨（Step-by-Step Approval）
1) research（market-insight-searcher / x-research-agent）
2) strategy（marketing-strategy-agent / social-growth-hacker）
3) creative（creative-director）
4) legal（legal-compliance-guard）

## 手順
1. 目的（Goal）を1行で確定：認知 / 新規獲得 / 復帰 のいずれか。
2. ターゲット（誰のどんな不満を解くか）を1つに絞る。
3. キャンペーンコンセプト（1行）＋メッセージ（3行）を作る。
4. チャネル設計（X/広告/コラボ）。
5. KPIツリー（上位→中位→下位）＋計測イベントを書く。
6. 制作物リスト＋制作順。
7. 1週間の実行計画（Day1〜Day7）。
8. リスクと対策（炎上/権利/誇大/運用負荷）。
9. 保存：
   - `ideas/[YYYYMMDD]-[theme].md`（中間）
   - `output/reports/[YYYY-MM-DD]-campaign-[theme].md`（最終）

## テンプレ
- `templates/campaign-brief.md`

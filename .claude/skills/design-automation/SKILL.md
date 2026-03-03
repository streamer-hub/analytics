---
name: design-automation
description: APIを活用したマーケ自動化ワークフロー（取得→加工→生成→投稿→計測）を設計し、実装に渡せる仕様として保存します。
argument-hint: [workflow-goal]
disable-model-invocation: true
---
# design-automation

StreamerHubの「APIを活用した自動化ワークフロー」を設計するスキルです。

## サブエージェント推奨
- technical-marketing-agent（技術→ベネフィット/実装要件）
- marketing-strategy-agent（KPI/優先度）
- legal-compliance-guard（規約/権利）

## 手順
1. ゴールを1行で確定（`$ARGUMENTS`）。
2. 入力データ（ソース）を列挙：DB/API/Web/手入力。
3. 処理ステップを分解：取得→正規化→生成→レビュー→配信→計測。
4. 失敗時の挙動（リトライ/手動介入/ログ）を決める。
5. 最小MVP（1週間で作れる）を定義。
6. 計測イベントと成功基準（KPI）を定義。
7. 保存：
   - `output/specs/automation/[YYYY-MM-DD]-[workflow].md`

## テンプレ
- `templates/automation-workflow.md`

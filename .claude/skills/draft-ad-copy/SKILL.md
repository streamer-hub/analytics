---
name: draft-ad-copy
description: 広告文（Google/Youtubeなど）をヘッドラインと説明文に分けて作成し、レビュー後に output/ads/ に保存します。
argument-hint: [campaign-or-feature]
disable-model-invocation: true
---
# draft-ad-copy

広告文を「Headline」と「Description」に分け、複数案を用意します（Agentic Workflowの実装）。

## サブエージェント推奨
- creative-director（案）
- technical-marketing-agent（技術→ベネフィット翻訳）
- legal-compliance-guard（最終チェック）

## 手順
1. キャンペーン対象（機能/イベント/サービス）を確定（`$ARGUMENTS`）。
2. 目的を確定：認知 / クリック / 登録 のどれか。
3. ターゲットを1つ決める（配信視聴者/配信者/イベント追従層 など）。
4. クリエイティブ案を作成：
   - Headline: 10〜15案
   - Description: 6〜10案
   - バリエーション軸：機能訴求 / 時短 / 体験 / 社会的証拠 / 緊急性
5. 技術要素がある場合は「ベネフィット」へ翻訳して差し替える。
6. 法務観点でNGを除外・弱める（断定/比較/権利）。
7. 保存：
   - `output/ads/[YYYY-MM-DD]-[campaign].md`
   - （任意）`output/ads/[YYYY-MM-DD]-[campaign].csv`（アップロード用）

## テンプレ
- `templates/ad-copy.md`
- `templates/ad-copy.csv`

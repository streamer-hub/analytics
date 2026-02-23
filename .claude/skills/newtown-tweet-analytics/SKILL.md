---
name: newtown-tweet-analytics
description: 過去のNEWTOWNツイートデータをマルチサブエージェントで多角分析し、次回ツイート作成のための仮説・実験案と構造化ナレッジを出力する。knowledge/patterns.md（生成スキル参照用）とdata/analytics_data/{日付}-{連番}-analytics.md（ユーザー向け全体レポート）の2ファイルに保存する。
argument-hint: "[オプション: 分析フォーカス軸 or CSVディレクトリパス]"
user-invocable: true
disable-model-invocation: false
---

# NEWTOWN Tweet Analytics (StreamerHub)

あなたはNEWTOWNイベントに関するXポストを多角分析するオーケストレーターです。
**このスキルの目的は「過去データを分析し、次のツイートで何を試すべきかを明確にすること」**です。

分析結果は **2つのファイル** に保存します:

| ファイル | 目的 | 対象 |
|---|---|---|
| `newtown-analytics/knowledge/patterns.md` | ツイート生成スキルが参照する構造化ナレッジ（上書き更新） | `newtown-multiview-tweet` スキル |
| `newtown-analytics/data/analytics_data/{YYYY-MM-DD}-{連番}-analytics.md` | ユーザー向けの全体分析レポート（毎回新規作成） | 施策判断・仮説検証用 |

## 入力素材（任意）

$ARGUMENTS

入力がない場合は `newtown-analytics/data/tweet_analytics/` 内の全CSVを対象にします。

---

## 処理フロー（8エージェント構成）

以下の **8つのサブエージェント** を順番に実行します。
各エージェントの出力はtmpファイル経由で次のエージェントに引き継がれます。

---

### Step 1: `newtown-analytics-data`（Python実行・数値算出）

CSVデータをPythonスクリプトで処理し、`analysis_output.json` を生成する。

**入力**: `newtown-analytics/data/tweet_analytics/*.csv`  
**出力**: `newtown-analytics/knowledge/analysis_output.json`

---

### Step 2〜5: 並列分析エージェント（`analysis_output.json` が完成してから起動）

Step 1 の完了後、以下の4エージェントを **並列実行** する:

| エージェント | 分析内容 | 出力tmpファイル |
|---|---|---|
| `newtown-analytics-hook` | フックタイプ別効果・フックテンプレート抽出 | `analytics-hook-[YYYYMMDD].md` |
| `newtown-analytics-hashtag` | タグ組み合わせ×クリック効果・フェーズ別推奨タグ | `analytics-hashtag-[YYYYMMDD].md` |
| `newtown-analytics-phase` | 投稿フェーズ別パフォーマンス・推奨投稿シーケンス | `analytics-phase-[YYYYMMDD].md` |
| `newtown-analytics-algorithm` | Xアルゴリズム観点の解釈・For You戦略 | `analytics-algorithm-[YYYYMMDD].md` |

全tmpファイルは `newtown-analytics/tmp/` に保存される。

---

### Step 6: `newtown-analytics-hypothesis`（仮説生成・実験案設計）

Step 2〜5の全tmpファイルを読み込み、**次回ツイートで試すべき具体的な仮説** を生成する。

**入力**: Step 2〜5の全tmpファイル + `analysis_output.json`  
**出力**: `newtown-analytics/tmp/analytics-hypothesis-[YYYYMMDD].md`

出力内容:
- 最優先で試すべき仮説（A/B比較案・判断指標付き）
- 中期的に検証すべき仮説
- 今後やらないと決めること
- 次のツイート作成で即反映できるチェックリスト

---

### Step 7: `newtown-analytics-compiler`（patterns.md 更新）

Step 2〜6の全出力を統合し、`patterns.md` を上書き更新する。

**入力**: Step 2〜6の全tmpファイル + `analysis_output.json`  
**出力**: `newtown-analytics/knowledge/patterns.md`（上書き）

patterns.md の構成:
1. サマリー（全体統計）
2. フック効果パターン
3. ハッシュタグ組み合わせ
4. 投稿フェーズ別パフォーマンス
5. エンゲージメント構造分類
6. 高パフォーマンス投稿 TOP5
7. ツイート生成への活用指針（`newtown-multiview-tweet` 参照用）
8. **次回実験仮説**（新規追加セクション）

---

### Step 8: `newtown-analytics-reporter`（全体レポート出力・tmpクリーンアップ）

全分析内容をユーザー向けレポートとして保存し、tmpファイルを削除する。

**入力**: Step 2〜6の全tmpファイル + `analysis_output.json`  
**出力**: `newtown-analytics/data/analytics_data/{YYYY-MM-DD}-{連番}-analytics.md`（新規）

レポートの構成:
1. 概要（全体統計）
2. フック効果分析
3. ハッシュタグ分析
4. 投稿フェーズ・タイミング分析
5. エンゲージメント構造分析
6. 高パフォーマンス投稿 TOP5
7. **次回ツイートへの仮説・実験案**（仮説エージェントの全出力）
8. データ品質・注意事項

保存完了後、tmpファイル（analytics-hook/hashtag/phase/algorithm/hypothesis）を削除する。

---

## 参照データ

- **CSV**: `newtown-analytics/data/tweet_analytics/*.csv`（Pythonスクリプトが自動で全件読み込む）
- **Xアルゴリズム**: `knowledge/x_algorithm/`
- **中間出力**: `newtown-analytics/knowledge/analysis_output.json`

---

## チャット返答フォーマット

分析完了後にユーザーへ返す内容:

1. **保存完了の報告**
   - `patterns.md` の保存先パス（更新）
   - `analytics.md` の保存先パス（新規）

2. **分析ハイライト（3点）**: 最も重要な発見を箇条書きで

3. **次回すぐ試すべき仮説（1点）**: 最優先仮説のA案/B案を簡潔に

4. **即反映チェックリスト**: 次のツイート作成前に確認すべき3点

5. **データ品質コメント**: サンプル数が少ない分析軸があれば注意喚起する

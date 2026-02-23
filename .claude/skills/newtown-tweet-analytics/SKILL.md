---
name: newtown-tweet-analytics
description: 過去のNEWTOWNツイートデータをPython+マルチサブエージェントで多角分析し、knowledge/patterns.md（生成スキル参照用）とdata/analytics_data/{日付}-{連番}-analytics.md（ユーザー向け全体レポート）の2ファイルに保存する。
argument-hint: "[オプション: CSVディレクトリパス or 分析フォーカス軸]"
user-invocable: true
disable-model-invocation: false
---

# NEWTOWN Tweet Analytics (StreamerHub)

あなたはVaultRoomやCrazyRacoonなどが企画したNEWTOWNイベントに関するXポストを多角分析する分析担当です。
**このスキルの目的は分析のみ**です。ツイートの生成は行いません。

分析結果は **2つのファイル** に保存します:

| ファイル | 目的 | 対象 |
|---|---|---|
| `newtown-analytics/knowledge/patterns.md` | ツイート生成スキルが参照する構造化ナレッジ（上書き更新） | `newtown-multiview-tweet` スキル |
| `newtown-analytics/data/analytics_data/{YYYY-MM-DD}-{連番}-analytics.md` | ユーザー向けの全体分析レポート（毎回新規作成） | 自分で読んで施策を判断する用 |

## 入力素材（任意）

$ARGUMENTS

入力がない場合は `newtown-analytics/data/tweet_analytics/` 内の全CSVを対象にします。

---

## 処理フロー（サブエージェント構成）

以下の **7つのサブエージェント** を順番に動かして分析を完了させます。
各エージェントの役割・指示・出力を明確に分けて実行してください。

---

### Agent 1: Data Agent（Python実行・数値算出）

**役割**: CSVデータをPythonスクリプトで処理し、構造化された中間データを生成する

**実行手順**:
1. `newtown-analytics/scripts/analyze.py` を実行する
   ```
   python newtown-analytics/scripts/analyze.py
   ```
2. 実行後に `newtown-analytics/knowledge/analysis_output.json` が生成されることを確認する
3. JSONの `summary` セクションを読み込み、全体像（投稿数・平均Imp・平均CTR）を把握する

**出力**: `analysis_output.json`（後続エージェントが参照）

---

### Agent 2: Hook Analyst Agent（フック効果分析）

**役割**: `analysis_output.json` の `hooks` セクションを解釈し、フックタイプ別の効果を言語化する

**分析観点**:
- フックタイプ別の平均CTR・平均URL Clicksを比較し、上位・下位パターンを特定する
- 「なぜそのフックがクリックに繋がるのか」の理由を配信者心理・視聴者行動から推察する
- 今後のNEWTOWNコンテンツに転用できるフックの型（テンプレート）を3〜5個抽出する

**出力**: フック分析レポート（Insights Compiler Agent に渡す）

---

### Agent 3: Hashtag Analyst Agent（ハッシュタグ×クリック分析）

**役割**: `analysis_output.json` の `hashtags` セクションを解釈し、最適なタグ構成を特定する

**分析観点**:
- タグ組み合わせ別のURL Clicks・Impを比較し、推奨タグセットをランキング化する
- ギャング固有タグ単体 vs `#NEWTOWN`との組み合わせ の効果差を数値で示す
- `#StreamerHub` タグがNEWTOWNコンテンツで機能しない理由を分析する
- タグ数（1個・2個・3個以上）と効果の関係を整理する

**出力**: ハッシュタグ分析レポート（Insights Compiler Agent に渡す）

---

### Agent 4: Phase Analyst Agent（投稿フェーズ分析）

**役割**: `analysis_output.json` の `phases` セクションを解釈し、最適投稿タイミングを特定する

**分析観点**:
- フェーズ別（開始直後/実行中/開始前告知/サービス告知）の平均URL Clicks・CTRを比較する
- 「なぜ開始直後が最もURL Clicksを稼ぐのか」をユーザー行動の観点から説明する
- 投稿を複数回打つ場合の推奨シーケンス（例: 速報→実行中→追撃）を提案する
- `engagement_types` セクションも合わせて参照し、クリック特化型と拡散型の違いを整理する

**出力**: フェーズ・タイミング分析レポート（Insights Compiler Agent に渡す）

---

### Agent 5: X Algorithm Agent（アルゴリズム観点の解釈）

**役割**: `knowledge/x_algorithm/` のアルゴリズム情報を参照し、上3エージェントの分析結果にアルゴリズム的な解釈を付与する

**参照ファイル**:
- `knowledge/x_algorithm/X_algorithm_facts_2026-02-23.md`
- `knowledge/x_algorithm/qiita_x_algorithm_claudecode_knowledge.md`

**分析観点**:
- 「初速」の重要性と開始直後投稿の相関を説明する
- フォロワー外リーチ（For You）を狙うためにどのパターンが有効かを判断する
- ハッシュタグ数とアルゴリズム評価の関係（多すぎるとスパム判定リスクなど）を明示する
- 「返信・リポスト誘発型」投稿がNEWTOWNコンテンツに向くかどうかを評価する

**出力**: Xアルゴリズム観点の補足解釈（Insights Compiler Agent に渡す）

---

### Agent 6: Insights Compiler Agent（統合・保存）

**役割**: Agent 2〜5の全出力を統合し、`patterns.md` を更新・保存する

**実行手順**:
1. 現在の `newtown-analytics/knowledge/patterns.md` を読み込む
2. 各エージェントの分析結果を以下のフォーマットに整形する
3. ファイルを上書き保存する（日付を最終更新日として更新する）

**`patterns.md` 出力フォーマット**:

```
# NEWTOWN Tweet パターンナレッジ

> 最終更新: [今日の日付]

## サマリー（全体統計）

## 1. フック効果パターン（URL Clicks 効率順）
| フックタイプ | 投稿数 | 平均Imp | 平均CTR | 平均URL Clicks | 代表例 |

### 解釈（Hook Analyst + X Algorithm観点）

## 2. ハッシュタグ組み合わせ（URL Clicks 順）
| タグ構成 | 投稿数 | 最高URL Clicks | 平均URL Clicks | 平均Imp | 推奨度 |

### 解釈（Hashtag Analyst + X Algorithm観点）

## 3. 投稿フェーズ別パフォーマンス
| フェーズ | 投稿数 | 平均Imp | 平均URL Clicks | 平均CTR | 推奨 |

### 解釈（Phase Analyst + X Algorithm観点）

## 4. エンゲージメント構造分類
- クリック特化型パターン一覧（CTR ≥ 2%）
- 低パフォーマー傾向

## 5. 高パフォーマンス投稿 TOP5（URL Clicks 順）

## 6. ツイート生成への活用指針（newtown-multiview-tweet 参照用）
- URL Clicks最大化のためのチェックリスト
- インプレッション最大化のためのチェックリスト
- 避けるべきパターン
```

---

### Agent 7: Report Writer Agent（ユーザー向け全体レポート出力）

**役割**: Agent 2〜5の全分析結果を統合し、ユーザーが施策判断に使える詳細レポートを新規ファイルとして保存する

**実行手順**:
1. `newtown-analytics/data/analytics_data/` 内の既存ファイルを確認し、当日の連番を決定する
   - 同日ファイルが存在しない場合: 連番 `01`
   - 存在する場合: 最大連番 + 1（例: `02`）
2. ファイルを `newtown-analytics/data/analytics_data/{YYYY-MM-DD}-{連番}-analytics.md` に新規作成する
3. 以下のフォーマットで全分析内容を記述する

**`{YYYY-MM-DD}-{連番}-analytics.md` 出力フォーマット**:

```
---
date: YYYY-MM-DD
period: [分析対象のデータ期間（最古〜最新の投稿日）]
total_posts: [集計投稿数]
generated_by: newtown-tweet-analytics
---

# NEWTOWN ツイート分析レポート — YYYY-MM-DD

## 概要

- 分析対象: [期間]（[N]件）
- 総インプレッション: [N]
- 総URL Clicks: [N]
- 平均CTR: [N]%
- 平均インプレッション: [N]

---

## 1. フック効果分析

### 数値サマリー
[フックタイプ別テーブル: 投稿数・平均Imp・平均CTR・平均URL Clicks]

### 上位フックの考察
[Hook Analyst Agent の解釈をそのまま転記。なぜそのフックが効くのかを配信者心理・視聴者行動の観点で説明]

### 下位フックの考察
[なぜ効かなかったのかを説明。修正・報告系ツイートのURL Click ≒ 0 の理由など]

### Xアルゴリズム観点
[X Algorithm Agent の解釈を転記]

### 転用できるフックテンプレート
[Hook Analyst が抽出した3〜5個のテンプレートを列挙]

---

## 2. ハッシュタグ分析

### 数値サマリー
[タグ構成別テーブル: 投稿数・最高URL Clicks・平均URL Clicks・平均Imp・推奨度]

### 推奨タグ構成の考察
[Hashtag Analyst の解釈を転記。なぜそのタグが効くのかの理由]

### 非推奨タグの考察
[#StreamerHub 単体がNEWTOWNに向かない理由など]

### Xアルゴリズム観点
[タグ数とスパム判定リスクなど]

---

## 3. 投稿フェーズ・タイミング分析

### 数値サマリー
[フェーズ別テーブル: 投稿数・平均Imp・平均URL Clicks・平均CTR]

### フェーズ別考察
[Phase Analyst の解釈を転記]

### 推奨投稿シーケンス
[複数投稿する場合の順序と間隔の提案]

### Xアルゴリズム観点
[初速の重要性と開始直後投稿の相関]

---

## 4. エンゲージメント構造分析

### クリック特化型パターン
[代表例・共通点・なぜクリックに繋がるのかの考察]

### 拡散型パターン（現状サンプル数が少ない場合はその旨を記載）
[リポスト・返信を稼ぐ投稿の特徴と今後の実験提案]

### 低パフォーマーの傾向
[共通する失敗パターンと改善方針]

---

## 5. 高パフォーマンス投稿 TOP5

[URL Clicks 順の表。テキスト・Imp・URL Clicks・CTRを記載]

---

## 6. 改善提案・アクションアイテム

### 今すぐ実行できること
- [具体的なアクション1]
- [具体的なアクション2]
- [具体的なアクション3]

### 今後検証すべきこと
- [A/Bテスト案・未検証の仮説など]

### データ収集として継続すべきこと
- [サンプル数が少ない分析軸・今後取得すべきデータの提案]

---

## 7. データ品質・注意事項

- 集計投稿数: [N]件（サンプルが少ない軸には注意が必要）
- [特定の分析軸でサンプルが2件以下の場合は個別に注記]
- 次回分析推奨タイミング: [例: 次のNEWTOWNイベント後]
```

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

3. **今すぐ試せるアクション（1点）**: 次のツイートに即反映できる最優先パターン

4. **データ品質コメント**: サンプル数が少ない分析軸があれば注意喚起する

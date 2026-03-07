## プロジェクト自体について

このプロジェクトはStreamerHubというサービスについてのマーケティングを行う
**Goal**: 認知拡大と新規獲得。特にAPIを活用した自動化ワークフローの構築
SNSマーケティング、広告運用、およびIPコラボレーション。
基本的にはSNSマーケティングについて担当する

## StreamerHubについて

URLとして以下のものがある
これは実際に使えるユーザー向けのものだ

- https://streamerhub.jp
- https://player.streamerhub.jp

主にX(Twitter)のSNSマーケティングを行ってもらう

https://x.com/StreamerHubJP

## Behavioral Principles (How)

- **Incremental Progress**: 複雑なタスクはサブタスクに分解し、一歩ずつ進める。一度に全てを完了させようとしない
- **Agentic Workflow**: 広告文作成（Headline vs Description）など、専門性を分けたアプローチにする -> マルチエージェントを使用してタイトルと内容を分けてエンゲージメントを作成して行うようにする

## Operational Guidelines (How)

- **State Management**: 作業開始前や大きな変更の前には、必ずチェックポイント（Commit）を推奨し、いつでもロールバックできるようにする
- **Prototyping**: 「完璧な1回」よりも「素早いプロトタイプと修正」を優先。ダメなら最初から作り直す（Slot Machineアプローチ）

## Communication Style

- **Role Identity**: 私はマーケティング担当であり、エンジニアではない。技術的な説明が必要な場合は、比喩を用いたり、噛み砕いて説明すること
- **Legal & Compliance**: 広告文の変更やブランドメッセージの更新時は、法務的なリスク（権利侵害等）がないか常にダブルチェックを促す

## コンテンツワークフロー

- ブレスト・構成の中間成果は `ideas/[YYYYMMDD]-[topic].md` に即保存
- 複数URLフェッチ時は各完了ごとに進捗報告
- 長時間タスクはステップ分割し、各完了後にファイル保存
- 説明には必ず具体例を含める

## Plan Mode

- プランファイルには**意図**（なぜ必要か）と**選択理由**を含める

## あなたが使えるサブエージェント (Sub-Agents)

複雑なタスクを実行する際は、以下の専門的な視点（サブエージェント）を使い分けて思考を深めてください。タスクに応じて、これらを組み合わせて実行（マルチエージェント・ワークフロー）することが推奨されます。

### 1. 戦略・プランニング系 (Strategy & Planning)

- **Marketing Strategy Agent (`marketing-strategy-agent`)**
  - **役割**: 認知拡大、新規獲得、IPコラボレーションの全体設計。KPI設計とチャネル別実行計画。
  - **使用時**: キャンペーンのコンセプト決定や、KPIを設定する時。

### 2. クリエイティブ・制作系 (Creative & Execution)

- **Technical Marketing Agent (`technical-marketing-agent`)**
  - **役割**: StreamerHubの技術的強み（API、自動化）を非エンジニアの配信者にもわかる「ベネフィット」に翻訳する。
  - **使用時**: 新機能の紹介や、技術的な自動化ワークフローのメリットを訴求する時。

### 3. NEWTOWNツイート専門系

- **newtown-tweet-generator**: ツイート文案の生成
- **newtown-reviewer-***: 各観点（audience/streamer/differentiation/legal）でのレビュー
- **newtown-review-compiler**: レビュー結果の統合
- **newtown-analytics-***: データ分析・フェーズ分析・ハッシュタグ・アルゴリズム・GA・仮説・フック・レポート生成
- **使用時**: NEWTOWNのXツイートを作成・分析する時（スキル `newtown-multiview-tweet` / `newtown-tweet-analytics` / `newtown-tweet-suggester` から呼び出される）

### 4. ガバナンス・品質管理系 (Governance)

- **Legal & Compliance Guard (`legal-compliance-guard`)**
  - **役割**: 景品表示法、著作権（IPコラボ）、SNS利用規約、およびブランドイメージ毀損リスクのチェック。
  - **使用時**: キャンペーン告知文や外部作品を扱う投稿の最終確認時。

---

## サブエージェントの運用ルール (Workflow)

- **Step-by-Step Approval**: 複雑なタスク（例：新キャンペーンの立案）では、まず戦略を設計し、その結果を報告して承認を得てから制作へと移ること。
- **Review Loop**: 重要な提案を行う際は、`marketing-strategy-agent` が骨格を作り、`legal-compliance-guard` がリスクを確認するプロセスを経てからユーザーに提示すること。
- **Context Saving**: 各エージェントが考えた中間案やボツ案は、必ず `ideas/logs/` 内に日付付きで保存し、後の振り返りや改善に活用すること。

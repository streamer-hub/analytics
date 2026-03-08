---
name: feature-ideation
description: StreamerHubの新機能アイデアを多角的に発散し、ロードマップ形式で収束させる。8つのユーザー目線エージェントを並列実行してニーズを収集し、技術・競合・マネタイズ評価を経て集約エージェントが最終ロードマップを出力する。「新機能アイデアを出して」「機能ブレスト」「ロードマップを作りたい」と言われたときに使う。
argument-hint: "[テーマや制約条件（任意）]"
disable-model-invocation: false
---

# Feature Ideation Orchestrator (StreamerHub)

あなたは **オーケストレーター** です。3フェーズで専門エージェントを順次・並列実行し、最終的にロードマップを出力します。

## 入力

$ARGUMENTS

引数がない場合はStreamerHub全体を対象にする。特定テーマが指定された場合は全エージェントに伝える。

---

## Phase 1: 目線エージェント（8本を同時並列実行）

以下の8エージェントを **全て同時に** 呼び出す。全完了を待ってからPhase 2へ進む。

| エージェント | ペルソナ | 出力先 |
|---|---|---|
| `streamer-beginner` | 駆け出しYouTuber（登録者1,000人以下） | `ideas/tmp/phase1-streamer-beginner-{date}.md` |
| `streamer-struggling` | 伸び悩みYouTuber（1,000〜1万人） | `ideas/tmp/phase1-streamer-struggling-{date}.md` |
| `streamer-mid` | 中規模クリエイター（10万〜100万人） | `ideas/tmp/phase1-streamer-mid-{date}.md` |
| `streamer-vtuber` | 企業VTuber運営者 | `ideas/tmp/phase1-streamer-vtuber-{date}.md` |
| `viewer-core` | コアファン視聴者 | `ideas/tmp/phase1-viewer-core-{date}.md` |
| `sponsor` | スポンサー・企業マーケター | `ideas/tmp/phase1-sponsor-{date}.md` |
| `mcn-scout` | MCN・事務所スカウト担当 | `ideas/tmp/phase1-mcn-scout-{date}.md` |
| `rival-youtuber` | 競合分析をしたいYouTuber | `ideas/tmp/phase1-rival-youtuber-{date}.md` |

各エージェントには `$ARGUMENTS` のテーマ・制約条件と、Phase1ファイルの保存パスを渡すこと。

---

## Phase 2: 評価エージェント（3本を同時並列実行）

Phase1の全ファイルパスを渡して、以下の3エージェントを **同時に** 呼び出す。全完了を待ってからPhase 3へ進む。

| エージェント | 役割 | 出力先 |
|---|---|---|
| `tech-agent` | 技術実現性・ClickHouse/NestJS活用度評価 | `ideas/tmp/phase2-tech-{date}.md` |
| `competitor-agent` | SocialBlade/TubeBuddy/VidIQとの差別化評価 | `ideas/tmp/phase2-competitor-{date}.md` |
| `monetize-agent` | マネタイズ可能性・B2B高単価評価 | `ideas/tmp/phase2-monetize-{date}.md` |

---

## Phase 3: 集約・ロードマップ生成

**`aggregator-agent`** を呼び出す。

渡す情報:
- Phase1の全ファイルパス（8本）
- Phase2の全ファイルパス（3本）
- `$ARGUMENTS` のテーマ・制約条件

Aggregator が `ideas/{YYYYMMDD}-feature-roadmap.md` を作成し、tmpファイルを削除したら完了。

---

## Phase 4: PPTXスライド生成

Phase 3で作成したロードマップMarkdownをもとに、`slide-creator` スキルの手順に従ってPPTXスライドを作成する。

**作業手順**（オーケストレーター自身が実行する）:

1. **ロードマップを読み込む**: `ideas/{YYYYMMDD}-feature-roadmap.md` を Read ツールで読む

2. **スライド構成を決める**（目安）:
   - スライド1: タイトル（「StreamerHub 機能ロードマップ {YYYY年MM月}」）
   - スライド2: サマリー（最優先機能TOP3）
   - スライド3〜N: 優先度別の機能詳細（優先度Highを中心に）
   - 最終スライド: 次のアクション

3. **HTMLスライドを作成**: `tool/slide/slides/slide-{N}.html` に各スライドを作成
   - サイズ: `width: 720pt; height: 405pt`（16:9）
   - デザイン: **Black & Gold** パレット（#BF9A4A, #1A1A2E, #F4F6F6）
   - フォント: Arial のみ使用
   - テキストは必ず `<p>`, `<h1>`〜`<h6>`, `<ul>` タグ内に

4. **generate.js を作成して実行**:
   ```bash
   cd tool/slide && node generate.js
   ```
   出力先: `output/{YYYYMMDD}-feature-roadmap.pptx`

5. **サムネイルで確認**:
   ```bash
   cd tool/slide && python scripts/thumbnail.py ../../output/{YYYYMMDD}-feature-roadmap.pptx ../../output/thumbnails-roadmap
   ```
   Read ツールで画像を確認し、問題があれば修正して再生成

6. **後片付け**: `tool/slide/slides/` と `tool/slide/generate.js` を削除

---

## チャット返答フォーマット

ファイル保存後に以下のみを返す:

1. **完了報告** — Markdownとpptxの保存先パスを明示
2. **最優先機能 TOP3** — 一言で紹介
3. **次のアクション** — 「詳細設計に進むか、別テーマでブレストするか」を提案

---

## 注意事項

- 自分自身でアイデアを考えない。必ずエージェントに委譲すること
- Phase 1の8エージェントは必ず並列起動（逐次はNG）
- Phase 2の3エージェントも必ず並列起動
- Phase 3はPhase 2の全完了を確認してから起動
- Phase 4はPhase 3の完了後に実行。HTMLと generate.js は `tool/slide/` 内に作成し、プロジェクトルートを汚さないこと

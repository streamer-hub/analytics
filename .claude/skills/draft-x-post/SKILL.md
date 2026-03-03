---
name: draft-x-post
description: X(Twitter)向け投稿案を作成し、Creative→Algorithm→Legalのレビューを回した上で、MarkdownとJSONLで保存します。
argument-hint: [topic-or-url]
disable-model-invocation: true
---
# draft-x-post

Xでの認知拡大/新規獲得向けに、投稿案を「生成→最適化→法務チェック」まで一気通貫で作ります。

## サブエージェント推奨（Review Loop）
1. creative-director：案を作る
2. algorithm-hacker：X最適化の添削
3. legal-compliance-guard：リスク確認

## 手順
1. topic を確定（`$ARGUMENTS` が空ならユーザーに1つ質問）。
2. 先に `ideas/[YYYYMMDD]-[topic].md` を作り、狙い・仮説・素材URLを書いておく。
3. 投稿の「狙い」を決める：認知 / クリック / 保存 / リプ誘発 のどれか（優先順位付き）。
4. 3案生成（最低）
   - A: 短文（フック強め）
   - B: 説明重視（ベネフィット→証拠→CTA）
   - C: スレッド（3〜6ツイート）
5. algorithm-hacker 観点で修正（1行目、改行、CTA、リンク位置、ハッシュタグ数）。
6. legal-compliance-guard 観点で修正（誇大、比較表現、権利侵害、規約リスク）。
7. 保存（両方）
   - `output/tweets/[YYYY-MM-DD]-[topic].md`
   - `output/tweets/tweet-generated/[YYYY-MM-DD]-[topic].jsonl`

## Markdownのテンプレ
`templates/tweet-pack.md` を使用。

## JSONL
`schema/tweet-log.schema.json` を参照。**1行=1案**（A/B/Cなど）。複数案は複数行で保存する。

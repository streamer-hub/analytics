---
name: repurpose-content
description: 1つのネタ（URL/新機能/ニュース）を複数フォーマットに変換し、output/へ保存します。
argument-hint: [source-url-or-topic]
disable-model-invocation: true
---
# repurpose-content

「1ネタ→複数展開」をテンプレ化します。

## サブエージェント推奨
- repurposing-agent（変換）
- algorithm-hacker（X最適化）
- creative-director（コピー品質）

## 入力
- `$ARGUMENTS` に URL または topic を渡す

## 出力（最低セット）
1. X短文（1本）
2. Xスレッド（3〜6ツイート）
3. アンケート案（1本：選択肢4つ）
4. Shorts用台本（20〜35秒）
5. ブログ/記事のアウトライン（見出しだけでOK）

## 保存
- `output/reports/[YYYY-MM-DD]-repurpose-[topic].md`
- （必要なら）`output/tweets/[YYYY-MM-DD]-[topic].md` にも分割して保存

## テンプレ
- `templates/repurpose-pack.md`

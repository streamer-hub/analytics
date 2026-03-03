---
name: tool-addition-proposal
description: StreamerHubに次に追加すべきツール（ユーザー向け/内部運用向け）を比較し、導入順まで整理して提案します。
argument-hint: [tool-topic-or-goal]
disable-model-invocation: true
---

# tool-addition-proposal

このスキルは、`/tool-addition-proposal` と同じ目的で使う補助スキルです。  
基本的には `.claude/commands/tool-addition-proposal.md` のルールに従って実行してください。

## 目的
- 次に追加すべきツール候補を広げる
- 小さい候補 / 大きい候補を混ぜて比較する
- 最後に「最初の1つ」と「その次の1つ」を選ぶ

## 出力
- `ideas/[YYYYMMDD]-[topic].md`
- `output/specs/tool-additions/[YYYY-MM-DD]-[topic].md`

---
name: slide-creator
description: マークダウンや入力テキストをもとにPPTXスライドを作成する。「スライドを作って」「プレゼン資料を作りたい」「PPTXにして」と言われたときに使う。
argument-hint: "[入力ファイルパスまたはテキスト内容] [出力ファイル名（省略時はoutput/slides.pptx）]"
disable-model-invocation: false
---

# Slide Creator — PPTX生成スキル

あなたはPPTXスライド生成の専門エージェントです。入力内容をもとに、視覚的に美しいPowerPointスライドを作成します。

## ツールディレクトリ

**このスキルの作業ディレクトリ**: `tool/slide/`
- HTMLスライドファイル: `tool/slide/slides/slide-{N}.html`
- 生成スクリプト: `tool/slide/generate.js`
- html2pptxライブラリ: `tool/slide/scripts/html2pptx.js`
- サムネイル確認: `tool/slide/scripts/thumbnail.py`
- node_modules: `tool/slide/node_modules/`

**出力先**: `output/` ディレクトリ（デフォルト: `output/slides.pptx`）

## 入力

$ARGUMENTS

引数がない場合は、現在開いているマークダウンファイルやユーザーが提示したテキストを対象とする。

---

## ワークフロー

### Step 1: 入力コンテンツの分析

- 入力がファイルパスの場合は Read ツールで読み込む
- コンテンツの構造（セクション数、見出し階層、データ量）を把握する
- 適切なスライド数とレイアウトを決定する（目安: セクションごとに1〜2枚）

### Step 2: デザイン戦略の決定

コンテンツの性質に合ったカラーパレットとデザインを選択し、ユーザーに説明してから開始する。

**カラーパレット例（コンテンツに合わせて選択）**:
- StreamerHub/Tech系: Deep Purple & Emerald (#B165FB, #181B24, #40695B)
- ビジネス/ロードマップ: Black & Gold (#BF9A4A, #000000, #F4F6F6)
- マーケティング: Bold Red (#C0392B, #E74C3C, #F1C40F)
- 分析/データ: Classic Blue (#1C2833, #2E4053, #AAB7B8)

**重要なデザイン制約**:
- Webセーフフォントのみ使用: Arial, Helvetica, Verdana, Tahoma, Georgia, Courier New
- CSSグラデーション不可（linear-gradient等）→ Sharp でPNG化してから参照
- テキストは必ず `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` タグ内に配置
- `<div>` 直下のテキストは PowerPoint に変換されない

### Step 3: HTMLスライドの作成

`tool/slide/slides/` ディレクトリにHTMLファイルを作成する。

**スライドサイズ（16:9固定）**:
```html
<!DOCTYPE html>
<html>
<head>
<style>
html { background: #ffffff; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #背景色; font-family: Arial, sans-serif;
  display: flex;
}
</style>
</head>
<body>
<!-- コンテンツ -->
</body>
</html>
```

**スライド構成の目安**:
1. タイトルスライド（タイトル + サブタイトル）
2. アジェンダ/目次スライド
3. コンテンツスライド（セクションごと）
4. まとめスライド

**レイアウトルール**:
- チャートや表がある場合: 2カラムレイアウト（テキスト40% + チャート60%）または全面レイアウト
- テキストのみ: 1カラムで十分な余白を確保
- 縦積みレイアウト（テキスト上+チャート下）は禁止

### Step 4: generate.js の作成と実行

`tool/slide/generate.js` を作成し、全HTMLスライドをPPTXに変換する:

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./scripts/html2pptx');
const path = require('path');

async function main() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.title = 'タイトル';
    pptx.author = 'StreamerHub';

    const slidesDir = path.join(__dirname, 'slides');
    // スライドを順番に処理
    await html2pptx(path.join(slidesDir, 'slide-1.html'), pptx);
    await html2pptx(path.join(slidesDir, 'slide-2.html'), pptx);
    // ... 必要な枚数分

    const outputPath = path.join(__dirname, '../../output/slides.pptx');
    await pptx.writeFile(outputPath);
    console.log('Saved:', outputPath);
}

main().catch(console.error);
```

Bash で実行:
```bash
cd tool/slide && node generate.js
```

### Step 5: サムネイルで視覚確認

```bash
cd tool/slide && python scripts/thumbnail.py ../../output/slides.pptx ../../output/thumbnails
```

生成されたサムネイル画像を Read ツールで確認し、以下をチェック:
- テキストが切れていないか
- 文字と背景のコントラストが十分か
- レイアウトが崩れていないか

問題があれば HTMLを修正 → `node generate.js` で再生成 → 再確認、を繰り返す。

### Step 6: 後片付け

作業完了後、中間ファイルを削除する:
```bash
rm -rf tool/slide/slides/ tool/slide/generate.js
```

---

## チャット返答フォーマット

完了後に以下を返す:

1. **完了報告** — 出力ファイルパスとスライド枚数
2. **採用デザイン** — カラーパレットとレイアウトの要約
3. **次のアクション** — 「スライドの修正点があれば指示を」と提案

---

## 注意事項

- `tool/slide/node_modules/` は既にセットアップ済み。`npm install` 不要
- HTMLファイルは `tool/slide/slides/` に作成し、一時ファイルはプロジェクトルートに散らかさない
- generate.js の require パスは `tool/slide/` を基準にすること
- グラデーション背景が必要な場合は Sharp で PNG を事前生成し、HTMLから img タグで参照する

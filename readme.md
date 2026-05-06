# drum_score

ドラム演奏動画（YouTube URL またはローカルファイル）から楽譜画像を自動抽出し、HTML として保存するツール。

## セットアップ

```bash
# 依存関係インストール
uv sync
```

## 使い方

### Web UI（推奨）

```bash
uv run python run_web.py
```

ブラウザが自動で開く。

1. YouTube URL またはローカル動画ファイルを指定
2. 楽譜が映っている ROI（領域）を選択
3. 処理完了後、フレームを選択して保存

### CUI 版

```bash
uv run python run.py <YouTube_URL or 動画ファイルパス>
```

## 出力

- `tmp/pics/` に楽譜画像と HTML ファイルが保存される
- HTML はブラウザで開いて印刷・PDF 化できる

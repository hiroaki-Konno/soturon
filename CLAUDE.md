# drum_score

ドラム演奏動画（YouTube URL またはローカルファイル）から楽譜画像を自動抽出し、HTML として保存するツール。

## 起動

```bash
# Web UI（通常はこちら）
uv run python run_web.py

# CUI 版（レガシー）
uv run python run.py <YouTube_URL or 動画ファイルパス>
```

## パッケージ管理

**uv** で管理する。pip は使わない。

## フォルダ構成

```
drum_score/
├── app.py              # Flask アプリ・API エンドポイント
├── run_web.py          # Web UI 起動（ブラウザ自動オープン）
├── run.py              # CUI 版起動
├── settings.py         # config.ini を読んで定数を公開
├── config.ini          # パス・ログ等の設定
├── pyproject.toml / uv.lock
│
├── core/               # バックエンド処理
│   ├── processor.py    # メイン処理クラス（トリミング・ピーク判定・SSE）
│   ├── trimming.py     # フレームトリミング・画像保存
│   ├── downloader.py   # YouTube ダウンロード（yt-dlp）
│   ├── html_generator.py  # HTML・ZIP 生成
│   └── logger.py       # loguru 初期化
│
├── static/             # フロントエンド
│   ├── index.js        # トップページ（動画読み込み・ROI 選択）
│   ├── viewer.js       # フレーム選択ページ（SSE・保存）
│   └── style.css
│
├── templates/          # Jinja2 テンプレート
│   ├── index.html
│   └── viewer.html
│
├── docs/               # 詳細ドキュメント
│   ├── architecture.md # Processor / SSE イベント / HtmlGenerator
│   └── config.md       # config.ini の全設定項目
│
└── tmp/                # 実行時生成（Git 管理外）
    ├── videos/         # ダウンロード動画
    ├── frames/         # 一時フレーム画像
    ├── pics/           # 出力先（楽譜画像・HTML）
    └── logs/
```

## ドキュメント

- [アーキテクチャ](docs/architecture.md) — データフロー・Processor・SSE イベント・HtmlGenerator
- [設定ファイル](docs/config.md) — config.ini の全設定項目

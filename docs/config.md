# 設定ファイル（config.ini）

`settings.py` が読み込んで定数として公開する。直接 `config.ini` を編集すればよく、コードの変更は不要。

## [paths]

| キー | デフォルト | 説明 |
|---|---|---|
| `video_folder_path` | `./tmp/videos` | yt-dlp でダウンロードした動画の保存先 |
| `score_folder_path` | `./tmp/pics` | 楽譜画像・生成 HTML の出力先 |
| `pic_dir_path` | `./tmp/pics` | 旧 CUI 版が参照するフォルダ（現在は `score_folder_path` と同じ） |
| `debug_base_path` | `./tmp/pics/test/` | `recog_score*.py` のデバッグ出力先 |

## [tools]

| キー | デフォルト | 説明 |
|---|---|---|
| `ffmpeg_dir` | （空） | ffmpeg の bin ディレクトリ。システムの PATH が通っていれば空でよい |

## [processing]

| キー | デフォルト | 説明 |
|---|---|---|
| `default_interval_sec` | `3` | フレーム抽出間隔（秒）。小さくすると枚数が増え処理時間も増える |

## [logging]

| キー | デフォルト | 説明 |
|---|---|---|
| `log_level` | `INFO` | コンソール出力のログレベル。`DEBUG` にすると類似度の値が出る |
| `log_dir` | `./tmp/logs` | ログファイルの出力先。日付ごとにローテーション（30日保持） |

## [score_images]

旧楽譜認識コード（`recog_score*.py`）専用。現在の Web UI では使用しない。

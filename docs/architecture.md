# アーキテクチャ

## Web UI のデータフロー

```
index.html
  → POST /api/load     : 動画読み込み・プレビュー生成
  → POST /api/start    : バックグラウンド処理開始 → viewer.html へ遷移

viewer.html
  → GET  /api/events   : SSE でリアルタイム進捗受信
  → GET  /api/frame/<i>: フレーム画像取得
  → POST /api/save     : 選択フレームを保存 + HTML自動生成
  → GET  /api/open_html: 保存済みHTMLをデフォルトブラウザで開く
```

## Processor クラス（core/processor.py）

メイン処理を担うシングルトン。`app.py` が `_processor = Processor()` として保持する。

| メソッド | 説明 |
|---|---|
| `load(source)` | 動画読み込み・プレビュー生成（同期） |
| `start(pos1, pos2)` | バックグラウンドスレッドで処理開始 |
| `event_stream()` | SSE 用ジェネレータ。`queue.Queue` でリアルタイム配信 |
| `get_frame_path(i)` | i 番目のフレーム画像パスを返す |
| `save_selected(indices)` | 選択フレームを JPEG として保存 |
| `generate_html(folder)` | 保存フォルダから HTML を生成 |

### 処理の流れ（`_run` 内）

1. **トリミング**: `default_interval_sec` 間隔でフレームを抽出・切り抜き → `frame_added` を逐次 emit
2. **類似度計算**: imgsim でベクトル化し隣接フレーム間の距離を算出 → `comparison_progress` を逐次 emit
3. **ピーク判定**: 距離の局所最大値（凸）を True にする → `frame_classified` を emit

### SSE イベント一覧

| type | 主なフィールド | 説明 |
|---|---|---|
| `frame_added` | `index` | フレーム1枚のトリミング完了 |
| `trimming_done` | `total` | 全フレームのトリミング完了 |
| `comparison_start` | — | 類似度計算開始 |
| `comparison_progress` | `current`, `total` | 計算進捗 |
| `frame_classified` | `index`, `is_peak`, `distance` | ピーク判定結果 |
| `comparison_done` | — | 全処理完了 |
| `error` | `message` | エラー発生 |
| `stream_end` | — | ストリーム終了 |

## HtmlGenerator クラス（core/html_generator.py）

```python
gen = HtmlGenerator(
    title="曲名",
    image_paths=["曲名001.jpg", ...],  # HTMLから見た相対パス
    lyrics={0: "Aメロ", 3: "サビ"},    # 画像直後に <p> を挿入
)
gen.save(output_path)            # HTML保存
gen.to_zip(image_dir, out_path)  # HTML + 画像を ZIP 化（実装済み）
gen.to_pdf(output_path)          # PDF変換（スタブ: weasyprint 想定）
```

- `image_paths` は HTML と同じフォルダに画像を置く前提でファイル名のみ渡す
- `lyrics` は将来の歌詞挿入用拡張ポイント

import os
import queue
import threading
import time

import cv2
import imgsim
from loguru import logger

from core.downloader import download
from core.trimming import PosTrim
from settings import SCORE_FOLDER_PATH

_PREVIEW_PATH = "./tmp/preview.jpg"
_FRAMES_DIR = "./tmp/frames"
_MAX_DISPLAY_WIDTH = 1280
_VEC = imgsim.Vectorizer()


class Processor:
    def __init__(self):
        self._lock = threading.Lock()
        # load() が設定する値（ジョブをまたいで保持する）
        self._video_path = ""
        self._scale = 1.0
        self.title = ""
        self._job_reset()

    def _job_reset(self):
        """処理ジョブの状態のみリセットする。load() の結果（パス・スケール）は保持する。"""
        self._events: list[dict] = []
        self._queue: queue.Queue = queue.Queue()
        self._done = False
        self._frame_paths: list[str] = []

    # ------------------------------------------------------------------
    # 公開メソッド
    # ------------------------------------------------------------------

    def load(self, source: str) -> dict:
        """動画を読み込みプレビューフレームを生成する（同期）"""
        if os.path.isfile(source):
            self._video_path = source
            self.title = os.path.splitext(os.path.basename(source))[0]
        else:
            self._video_path, self.title = download(source)

        cap = cv2.VideoCapture(self._video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        target = min(int(fps * 30), total - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target)
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, frame = cap.read()
        cap.release()

        if orig_w > _MAX_DISPLAY_WIDTH:
            scale = _MAX_DISPLAY_WIDTH / orig_w
            display_frame = cv2.resize(frame, (_MAX_DISPLAY_WIDTH, int(orig_h * scale)))
            display_w, display_h = _MAX_DISPLAY_WIDTH, int(orig_h * scale)
        else:
            display_frame = frame
            display_w, display_h = orig_w, orig_h

        self._scale = orig_w / display_w

        os.makedirs(os.path.dirname(_PREVIEW_PATH), exist_ok=True)
        _, buf = cv2.imencode(".jpg", display_frame)
        with open(_PREVIEW_PATH, "wb") as f:
            f.write(buf.tobytes())

        return {
            "display_w": display_w,
            "display_h": display_h,
            "orig_w": orig_w,
            "orig_h": orig_h,
            "title": self.title,
        }

    def start(self, pos1: tuple, pos2: tuple) -> None:
        """バックグラウンドでトリミング + 比較処理を開始する"""
        with self._lock:
            self._job_reset()

        # プレビュー座標 → 元動画座標に変換
        s = self._scale
        real_pos1 = (int(pos1[0] * s), int(pos1[1] * s))
        real_pos2 = (int(pos2[0] * s), int(pos2[1] * s))

        threading.Thread(
            target=self._run, args=(real_pos1, real_pos2), daemon=True
        ).start()

    def get_frame_path(self, index: int) -> str:
        with self._lock:
            return self._frame_paths[index]

    def save_selected(self, indices: list[int]) -> str:
        folder = os.path.join(SCORE_FOLDER_PATH, self.title)
        frames = []
        for i in sorted(indices):
            frame = cv2.imread(self.get_frame_path(i))
            if frame is not None:
                frames.append(frame)
        PosTrim.save_image_files(frames, folder, self.title)
        return folder

    def event_stream(self):
        """SSE 用ジェネレータ。過去イベントをリプレイしてから新規イベントをリアルタイムで流す。"""
        with self._lock:
            past = list(self._events)
            done = self._done

        for ev in past:
            yield ev

        if done:
            yield {"type": "stream_end"}
            return

        while True:
            try:
                ev = self._queue.get(timeout=0.5)
                yield ev
            except queue.Empty:
                with self._lock:
                    if self._done and self._queue.empty():
                        yield {"type": "stream_end"}
                        break

    # ------------------------------------------------------------------
    # 内部処理
    # ------------------------------------------------------------------

    def _emit(self, event: dict) -> None:
        with self._lock:
            self._events.append(event)
        self._queue.put(event)

    def _run(self, pos1: tuple, pos2: tuple) -> None:
        try:
            cap = cv2.VideoCapture(self._video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            interval = round(PosTrim.DEFAULT_INTERVAL_SEC * fps)

            os.makedirs(_FRAMES_DIR, exist_ok=True)
            for f in os.listdir(_FRAMES_DIR):
                os.remove(os.path.join(_FRAMES_DIR, f))

            raw_frames: list = []

            # Step 1: トリミング（フレームを逐次追加）
            for frame_pos in range(interval, total_frames + interval, interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                ret, frame = cap.read()
                if not ret or frame is None:
                    continue

                trimmed = PosTrim.trim_image(frame, pos1, pos2)
                raw_frames.append(trimmed)

                idx = len(raw_frames) - 1
                path = os.path.join(_FRAMES_DIR, f"frame_{idx:03d}.jpg")
                _, buf = cv2.imencode(".jpg", trimmed)
                with open(path, "wb") as f_out:
                    f_out.write(buf.tobytes())

                with self._lock:
                    self._frame_paths.append(path)

                self._emit({"type": "frame_added", "index": idx})

            cap.release()
            self._emit({"type": "trimming_done", "total": len(raw_frames)})

            # Step 2: 類似度比較（ピーク判定）
            self._emit({"type": "comparison_start"})

            vecs = []
            distances: list = [None]
            total = len(raw_frames)

            for i, f in enumerate(raw_frames):
                vec = _VEC.vectorize(f)
                vecs.append(vec)
                if i > 0:
                    dist = imgsim.distance(vecs[i - 1], vec)
                    distances.append(dist)
                    logger.debug(f"類似度 [{i}]: {dist:.4f}")
                self._emit({"type": "comparison_progress", "current": i + 1, "total": total})

            is_peaks = self._compute_peaks(len(raw_frames), distances)

            for i, is_peak in enumerate(is_peaks):
                self._emit({
                    "type": "frame_classified",
                    "index": i,
                    "is_peak": is_peak,
                    "distance": float(distances[i]) if distances[i] is not None else None,
                })

            logger.info(
                f"全フレーム: {len(raw_frames)} 枚 / "
                f"ピーク: {sum(is_peaks)} 枚"
            )
            self._emit({"type": "comparison_done"})

        except Exception as e:
            logger.error(f"処理エラー: {e}")
            self._emit({"type": "error", "message": str(e)})
        finally:
            with self._lock:
                self._done = True

    @staticmethod
    def _compute_peaks(n: int, distances: list) -> list[bool]:
        """距離リストの局所最大値（凸）を True にしたブールリストを返す"""
        if n == 0:
            return []
        result = [False] * n
        result[0] = True
        for i in range(1, n):
            d = distances[i]
            prev_d = distances[i - 1]
            next_d = distances[i + 1] if i + 1 < len(distances) else None
            if prev_d is not None and d <= prev_d:
                continue
            if next_d is not None and d <= next_d:
                continue
            result[i] = True
        return result

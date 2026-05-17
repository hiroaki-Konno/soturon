import os
import shutil

import cv2
import imgsim
from loguru import logger

from settings import DEFAULT_INTERVAL_SEC


class PosTrim:
    DEFAULT_INTERVAL_SEC = DEFAULT_INTERVAL_SEC
    DEFAULT_VEC = imgsim.Vectorizer()

    @staticmethod
    def trim_image(frame, pos1, pos2):
        """ 画像のトリミングを座標指定で行う

        Parameters
        ----------
        frame: ndarray
            トリミングしたい動画のフレーム画像
        pos1 : tuple(int, int)
            切り抜きたい画像の角の座標(左上推奨)
        pos2 : tuple(int, int)
            切り抜きたい画像の角の座標(右下推奨)

        Returns
        -------
        ndarray
            フレーム画像からトリミングされた画像の一部

        """
        x1, y1 = min(pos1[0], pos2[0]), min(pos1[1], pos2[1])
        x2, y2 = max(pos1[0], pos2[0]), max(pos1[1], pos2[1])
        return frame[y1:y2, x1:x2]

    @classmethod
    def trim_video(cls, cap, pos1: tuple, pos2: tuple) -> tuple[list, list]:
        """動画をインターバルでトリミングし、全フレームとピーク候補フレームを返す

        Parameters
        ----------
        cap : cv2.VideoCapture
            cv2で読み込まれた動画
        pos1 : tuple[int, int]
            楽譜領域の左上ピクセル座標 (x, y)
        pos2 : tuple[int, int]
            楽譜領域の右下ピクセル座標 (x, y)

        Returns
        -------
        tuple[list[ndarray], list[ndarray]]
            (all_frames, peak_frames)
            all_frames  : インターバルで抽出した全トリミングフレーム
            peak_frames : 類似度が局所最大（凸）のフレーム（楽譜切替推定）
        """
        prop_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        prop_fps = cap.get(cv2.CAP_PROP_FPS)
        interval_frame = round(cls.DEFAULT_INTERVAL_SEC * prop_fps)
        vtr = cls.DEFAULT_VEC

        all_frames = []
        distances = [None]  # distances[i]: frames[i] と frames[i-1] の類似度距離
        prev_vec = None

        for frame_pos in range(interval_frame, prop_frame_count + interval_frame, interval_frame):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            trimmed = cls.trim_image(frame, pos1, pos2)
            vec = vtr.vectorize(trimmed)

            if prev_vec is not None:
                dist = imgsim.distance(prev_vec, vec)
                logger.debug(f"画像類似度: {dist:.4f}")
                distances.append(dist)

            all_frames.append(trimmed)
            prev_vec = vec

        peak_frames = cls._extract_peaks(all_frames, distances)
        logger.info(
            f"全フレーム: {len(all_frames)} 枚 / ピーク候補: {len(peak_frames)} 枚"
        )
        return all_frames, peak_frames

    @staticmethod
    def _extract_peaks(frames: list, distances: list) -> list:
        """距離の局所最大値（凸）に対応するフレームを返す。先頭フレームは常に含む。

        Parameters
        ----------
        frames : list[ndarray]
            トリミングフレームのリスト
        distances : list[float | None]
            distances[i] = frames[i] と frames[i-1] の類似度距離（distances[0] は None）
        """
        if not frames:
            return []

        peaks = [frames[0]]

        for i in range(1, len(frames)):
            d = distances[i]
            prev_d = distances[i - 1]
            next_d = distances[i + 1] if i + 1 < len(distances) else None

            if prev_d is not None and d <= prev_d:
                continue
            if next_d is not None and d <= next_d:
                continue

            peaks.append(frames[i])

        return peaks

    @staticmethod
    def save_image_files(score_images: list, folder_path: str, pic_name: str = "tmp_frame")-> None:
        """ 画像のリストを受け取り、画像ファイルとして保存する

        Parameters
        ----------
        score_images: list(ndarray)
            ndarryで表される画像のリスト
        folder_path: str
            実行するプログラムからの相対パスを渡すことを想定
        """
        # 空のディレクトリを作成
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path, exist_ok=True)

        # cv2.imwrite は非ASCIIパスを扱えないため imencode + open で保存
        for i, score_image in enumerate(score_images):
            file_path = os.path.join(folder_path, f"{pic_name}{i+1:03}.jpg")
            ret, buf = cv2.imencode('.jpg', score_image)
            if not ret:
                logger.error(f"画像エンコード失敗: {file_path}")
                break
            with open(file_path, 'wb') as f:
                f.write(buf.tobytes())
        logger.info(f"{len(score_images)} 枚の楽譜画像を保存しました: {folder_path}")

    def improve_interval():
        """トリミングのインターバル（フレーム間隔）を動的に調整する（未実装）"""
        pass

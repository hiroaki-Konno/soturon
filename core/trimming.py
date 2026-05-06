import cv2
import imgsim
import os
import shutil
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
    def compare_image_for_overlap(cls, score_images, score_vecs, trimmed_score):
        """ トリミングされたフレーム画像が前の楽譜画像と重複していないか比較する

        Parameters
        ----------
        score_images: list(ndarray)
            トリミングされた楽譜画像のリスト
        score_vecs: list(ndarray)
            score_imagesに格納された楽譜画像をベクトル化したもののリスト
        trimmed_score: ndarray
            トリミングされたフレーム画像

        Returns
        -------
        score_images: list(ndarray)
            トリミングされた重複していない楽譜画像のリストを返す
        score_vecs: list(ndarray)
            トリミングされた重複していない楽譜画像のをベクトル化したもののリストを返す
        """
        vtr = cls.DEFAULT_VEC

        # 最初の一枚はとりあえず追加
        if len(score_images)==0:
            score_images.append(trimmed_score)
            score_vecs.append(vtr.vectorize(trimmed_score))
            return score_images, score_vecs

        before_score_vec = score_vecs[-1]
        trimmed_score_vec = vtr.vectorize(trimmed_score)
        dist = imgsim.distance(before_score_vec, trimmed_score_vec)
        logger.debug(f"画像類似度: {dist:.4f}")

        # if distに条件をつける
        score_images.append(trimmed_score)
        score_vecs.append(trimmed_score_vec)
        return score_images, score_vecs

    @classmethod
    def trim_video(cls, cap, pos1: tuple, pos2: tuple):
        """動画のトリミングを行う

        Parameters
        ----------
        cap: cv2.VideoCapture
            cv2で読み込まれた動画
        pos1 : tuple[int, int]
            楽譜領域の左上ピクセル座標 (x, y)
        pos2 : tuple[int, int]
            楽譜領域の右下ピクセル座標 (x, y)

        Returns
        -------
        list(ndarray):
            トリミングされた楽譜画像のリスト
        """
        prop_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        prop_fps = cap.get(cv2.CAP_PROP_FPS)

        score_images = []
        score_vecs = []

        current_frame = 0
        interval_sec = cls.DEFAULT_INTERVAL_SEC
        interval_frame = round(interval_sec * prop_fps)

        for specified_frame_count in range(interval_frame, prop_frame_count+interval_frame, interval_frame):
            cap.set(cv2.CAP_PROP_POS_FRAMES, specified_frame_count)
            _ , frame = cap.retrieve()

            trimmed_score = cls.trim_image(frame, pos1, pos2)

            # 画像の重複に基づく追加などの処理
            score_images, score_vecs = cls.compare_image_for_overlap(score_images, score_vecs, trimmed_score)

            # 動画の尺(フレーム)が終わったら終了
            if prop_frame_count < current_frame:
                return score_images

        return score_images

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

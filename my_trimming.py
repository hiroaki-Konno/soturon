import cv2
import os
import shutil

from my_score_pos import ScorePosition

class PosTrim:
    DEFAULT_INTERVAL_SEC = 3
    # def __init__(self, file_path, pos1, pos2) -> None:
    #     """ 座標によるトリミング用のクラス

    #     Parameters
    #     ----------
    #     file_path : str
    #         動画ファイルへのパスを指定する
    #     pos1 : tuple(int)
    #         切り抜きたい画像の角の座標(左上推奨)
    #     pos2 : tuple(int)
    #         切り抜きたい画像の角の座標(右下推奨)
    #     interval_sec : int
        
    #     """
    #     self.video = cv2.VideoCapture(file_path)
    #     self.interval_sec = 1
    #     pass

    # クラス変数にアクセスしない、インスタンスに依存しない
    # -> staticmethod
    @staticmethod
    def trim_image(frame, pos1, pos2):
        """ 画像のトリミングを座標指定で行う

        Parameters
        ----------
        frame: ndarray
            トリミングしたい動画のフレーム画像
        pos1 : tuple(int)
            切り抜きたい画像の角の座標(左上推奨)
        pos2 : tuple(int)
            切り抜きたい画像の角の座標(右下推奨)
        
        Returns
        -------
        ndarray
            フレーム画像からトリミングされた画像の一部

        """
        x1, y1 = min(pos1[0], pos2[0]), min(pos1[1], pos2[1])
        x2, y2 = max(pos1[0], pos2[0]), max(pos1[1], pos2[1])
        return frame[y1:y2, x1:x2]
    
    # クラス変数にアクセスする、インスタンスに依存しない
    # -> classmethod
    @classmethod
    def trim_video(cls, cap):
        """ 動画のトリミングを行う
        動画内で楽譜位置が変更される場合はここで調整
        画像の重複チェック、インターバルの調整もここに含む

        Parameters
        ----------
        cap: cv2.VideoCapture
            画質が1920*1080のcv2で読み込まれた動画
        
        Returns
        -------
        list(ndarray):
            トリミングされた楽譜画像のリストを返す
        """
        # フレーム総数
        prop_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        prop_fps = cap.get(cv2.CAP_PROP_FPS)

        score_images = []
        current_frame = 0
        interval_sec = cls.DEFAULT_INTERVAL_SEC
        interval_frame = round(interval_sec * prop_fps)

        # 楽譜の範囲を指定
        # pos1, pos2 = (0,0), (1920, 1080)
        # pos1, pos2 = (0,0), (854, 480)
        # 本来ならforループ内で逐次変更しながらやる想定
        score_pos = ScorePosition()
        pos1, pos2 = score_pos.mock_get_pos()

        """ トリミング間隔を調整しながらやる場合の構造
        while 最終フレームまで: 
          for i in range(現在フレーム, 最終フレーム, 幅):
              トリミング処理、重複チェック、インターバル調整など
        return score_images """
        # トリミングの繰り返し処理
        for specified_frame_count in range(interval_frame, prop_frame_count+interval_frame, interval_frame):
            cap.set(cv2.CAP_PROP_POS_FRAMES, specified_frame_count)
            _ , frame = cap.retrieve()

            trimmed_score = cls.trim_image(frame, pos1, pos2)
            score_images.append(trimmed_score)

            if prop_frame_count < current_frame:
                return score_images
            
        return score_images
    
    @staticmethod
    def save_image_files(score_images: list, folder_path: str)-> None:
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

        # 画像をリストから保存
        for i, score_image in enumerate(score_images):
            file_path = os.path.join(folder_path, f"tmp_frame{i+1:02}.jpg")
            # print(file_path)
            is_succeed_to_save_file = cv2.imwrite(file_path, score_image)
            
            # 失敗した場合のメッセージ表示
            if not is_succeed_to_save_file:
                print("Failed to save image file.")
                break
        print("Succeed to save image file.")
        

    def improve_interval():
        pass
    # def __init__(self, param1, param2, param3):
    #     """Example of docstring on the __init__ method.

    #     The __init__ method may be documented in either the class level
    #     docstring, or as a docstring on the __init__ method itself.

    #     Either form is acceptable, but the two should not be mixed. Choose one
    #     convention to document the __init__ method and be consistent with it.

    #     Note
    #     ----
    #     Do not include the `self` parameter in the ``Parameters`` section.

    #     Parameters
    #     ----------
    #     param1 : str
    #         Description of `param1`.
    #     param2 : list(str)
    #         Description of `param2`. Multiple
    #         lines are supported.
    #     param3 : :obj:`int`, optional
    #         Description of `param3`.

    #     """
    #     pass
import cv2
import os
import sys
from core.trimming import PosTrim as pt
from settings import VIDEO_FOLDER_PATH, SCORE_FOLDER_PATH


def mock_get_frame(cap):
    """動画の30フレーム目を取得して返す（座標確認用のモック関数）

    Parameters
    ----------
    cap: cv2.VideoCapture
        cv2で読み込まれた動画オブジェクト

    Returns
    -------
    list(ndarray)
        取得したフレーム画像を格納したリスト
    """
    any_frame = 30
    cap.set(cv2.CAP_PROP_POS_FRAMES, any_frame)
    _ , frame = cap.retrieve()
    return [frame]

def mock_save_frame(score_images: list, folder_path: str, pic_name: str = "tmp_frame")-> None:
    """楽譜画像リストの先頭画像を1枚ファイルに保存する（座標確認用のモック関数）

    Parameters
    ----------
    score_images: list(ndarray)
        保存したい画像を格納したリスト（先頭の1枚のみ保存される）
    folder_path: str
        保存先フォルダのパス
    pic_name: str
        保存するファイルの基底名
    """
    file_path = os.path.join(folder_path, f"{pic_name}_loc_score.jpg")
    is_succeed_to_save_file = cv2.imwrite(file_path, score_images[0])

    if not is_succeed_to_save_file:
        print("Failed to save image file.")
        return

    print("Succeed to save image file.")

def main():
    """動画から楽譜画像をトリミングして保存するメイン処理"""
    video_name = "ギターと孤独と蒼い惑星／吉他與孤獨的藍色星球│DRUM COVER"
    path_to_video = os.path.join(VIDEO_FOLDER_PATH, video_name+".mp4")
    new_score_folder_name = "tmp_kodoku"
    path_to_save_score = os.path.join(SCORE_FOLDER_PATH, new_score_folder_name)
    pic_name = "tmp_kodoku"

    video = cv2.VideoCapture(path_to_video)

    if not video.isOpened():
        print("video is not opend in run.py")
        sys.exit()

    trimmed_socres = pt.trim_video(video, video_name)
    pt.save_image_files(trimmed_socres, path_to_save_score, pic_name)

if __name__ == "__main__":
    main()

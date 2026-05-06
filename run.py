import cv2
import os
import sys

from core.downloader import download
from core.trimming import PosTrim as pt
from ui.region_selector import select_region
from settings import SCORE_FOLDER_PATH


def main():
    if len(sys.argv) < 2:
        print("使い方: python run.py <YouTube_URL or 動画ファイルパス>")
        sys.exit(1)

    arg = sys.argv[1]

    if os.path.isfile(arg):
        filepath = arg
        title = os.path.splitext(os.path.basename(filepath))[0]
        print(f"ファイルを使用: {filepath}")
    else:
        print("動画をダウンロード中...")
        filepath, title = download(arg)
        print(f"ダウンロード完了: {filepath}")

    video = cv2.VideoCapture(filepath)
    if not video.isOpened():
        print("動画を開けませんでした")
        sys.exit(1)

    print("楽譜の範囲をウィンドウで選択してください")
    pos1, pos2 = select_region(video)
    print(f"選択した座標: pos1={pos1}, pos2={pos2}")

    trimmed_scores = pt.trim_video(video, pos1, pos2)
    video.release()

    score_folder = os.path.join(SCORE_FOLDER_PATH, title)
    pt.save_image_files(trimmed_scores, score_folder, title)


if __name__ == "__main__":
    main()

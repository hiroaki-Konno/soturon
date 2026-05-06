import cv2
import os
import sys
from loguru import logger

from core.logger import setup_logger
from core.downloader import download
from core.trimming import PosTrim as pt
from ui.region_selector import select_region
from settings import SCORE_FOLDER_PATH


def main():
    setup_logger()

    if len(sys.argv) < 2:
        logger.error("使い方: python run.py <YouTube_URL or 動画ファイルパス>")
        sys.exit(1)

    arg = sys.argv[1]

    if os.path.isfile(arg):
        filepath = arg
        title = os.path.splitext(os.path.basename(filepath))[0]
        logger.info(f"ファイルを使用: {filepath}")
    else:
        filepath, title = download(arg)

    video = cv2.VideoCapture(filepath)
    if not video.isOpened():
        logger.error(f"動画を開けませんでした: {filepath}")
        sys.exit(1)

    logger.info("楽譜の範囲をウィンドウで選択してください")
    pos1, pos2 = select_region(video)
    logger.info(f"選択した座標: pos1={pos1}, pos2={pos2}")

    trimmed_scores = pt.trim_video(video, pos1, pos2)
    video.release()

    score_folder = os.path.join(SCORE_FOLDER_PATH, title)
    pt.save_image_files(trimmed_scores, score_folder, title)


if __name__ == "__main__":
    main()

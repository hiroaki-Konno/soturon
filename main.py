import cv2
import sys
from my_trimming import PosTrim as pt

def main():
    # 画像の読み込み
    # video_name = "video"
    video_name = "480p-高嶺の花子さん_不朽の名作~"
    path_to_video = f'./data/{video_name}.mp4'
    # path_to_save_score = "./tmp"
    path_to_save_score = "./test_imgdist"
    video = cv2.VideoCapture(path_to_video)

    if not video.isOpened():
        print("video is not opend in main.py")
        sys.exit()
    
    trimmed_socres = pt.trim_video(video)
    pt.save_image_files(trimmed_socres, path_to_save_score)


if __name__ == "__main__":
    main()
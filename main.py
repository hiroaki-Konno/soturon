import cv2
import os
import sys
from my_trimming import PosTrim as pt

def main():
    # 画像の読み込み
    # video_name = "video"
    # video_name = "480p-高嶺の花子さん_不朽の名作~"
    video_name = "何故か着地が下手くそなアホウドリ"
    path_to_video = f'./videos/{video_name}.mp4'

    score_folder_path = "./pics"
    # folder_name = "tmp"
    new_score_folder_name = "test_ahodri"

    path_to_save_score = os.path.join(score_folder_path, new_score_folder_name)  

    # pic_name = "tmp_frame"
    pic_name = "tmp_ahodori"

    video = cv2.VideoCapture(path_to_video)

    if not video.isOpened():
        print("video is not opend in main.py")
        sys.exit()
    
    trimmed_socres = pt.trim_video(video)
    pt.save_image_files(trimmed_socres, path_to_save_score, pic_name)


if __name__ == "__main__":
    main()
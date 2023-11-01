import cv2
import os
import sys
from my_trimming import PosTrim as pt

VIDEO_FOLDER_PATH = "./videos"
SCORE_FOLDER_PATH = "./pics"


def mock_get_frame(cap):
    any_frame = 30
    cap.set(cv2.CAP_PROP_POS_FRAMES, any_frame)
    _ , frame = cap.retrieve()
    return [frame]

def mock_save_frame(score_images: list, folder_path: str, pic_name: str = "tmp_frame")-> None:
    file_path = os.path.join(folder_path, f"{pic_name}_loc_score.jpg")
    is_succeed_to_save_file = cv2.imwrite(file_path, score_images[0])
            
    # 失敗した場合のメッセージ表示
    if not is_succeed_to_save_file:
        print("Failed to save image file.")
        return
            
    print("Succeed to save image file.")

def main():
    # 画像の読み込み
    # video_name = "video"
    # video_name = ".test_何故か着地が下手くそなアホウドリ"
    video_name = "サマータイムレコード"

    # path_to_video = f'./videos/{video_name}.mp4'
    path_to_video = os.path.join(VIDEO_FOLDER_PATH, video_name+".mp4")

    # folder_name = "tmp"
    new_score_folder_name = "tmp_samareko"

    path_to_save_score = os.path.join(SCORE_FOLDER_PATH, new_score_folder_name)  

    # pic_name = "tmp_frame"
    pic_name = "tmp_samareko"

    video = cv2.VideoCapture(path_to_video)

    if not video.isOpened():
        print("video is not opend in main.py")
        sys.exit()
    
    # 本来の処理
    trimmed_socres = pt.trim_video(video, video_name)
    pt.save_image_files(trimmed_socres, path_to_save_score, pic_name)


if __name__ == "__main__":
    main()
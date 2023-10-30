import cv2
import os
import sys
from my_trimming import PosTrim as pt

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
    # video_name = "480p-高嶺の花子さん_不朽の名作~"
    video_name = ".test_何故か着地が下手くそなアホウドリ"
    path_to_video = f'./videos/{video_name}.mp4'

    score_folder_path = "./pics"
    # folder_name = "tmp"
    new_score_folder_name = "loc_score"

    path_to_save_score = os.path.join(score_folder_path, new_score_folder_name)  

    # pic_name = "tmp_frame"
    pic_name = "tmp_ahodori"

    video = cv2.VideoCapture(path_to_video)

    if not video.isOpened():
        print("video is not opend in main.py")
        sys.exit()
    
    # trimmed_socres = pt.trim_video(video)
    trimmed_socres = mock_get_frame(video)

    # pt.save_image_files(trimmed_socres, path_to_save_score, pic_name)
    mock_save_frame(trimmed_socres, path_to_save_score, pic_name)


if __name__ == "__main__":
    main()
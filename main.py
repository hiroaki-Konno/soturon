import cv2
from my_trimming import PosTrim as pt

def main():
    # 画像の読み込み
    path_to_video = './data/video.mp4'
    path_to_save_score = "./tmp"
    video = cv2.VideoCapture(path_to_video)
    trimmed_socres = pt.trim_video(video)
    pt.save_image_files(trimmed_socres, path_to_save_score)


if __name__ == "__main__":
    main()